import asyncio

from web3 import AsyncWeb3, WebSocketProvider
from web3.datastructures import AttributeDict
from web3._utils.events import event_abi_to_log_topic

from client import Client
from custom_logger import logger
from config import UNISWAP_V3_POOL_ABI


class UniswapMevBot:
    def __init__(
        self, client: Client, wss_provider: str, eth_usdt_pool_address: str, eth_dai_pool_address: str,
        spread_percentage_threshold: float
        ) -> None:
        self.client = client
        self.alchemy_wss_url = wss_provider
        self.eth_usdt_pool_address = eth_usdt_pool_address
        self.eth_usdt_price = 0
        self.usdt_decimals = 6
        self.eth_dai_pool_address = eth_dai_pool_address
        self.eth_dai_price = 0
        self.dai_decimals = 18
        self.spread_percentage_threshold = spread_percentage_threshold
        self.pool_contract = self.client.get_contract(abi=UNISWAP_V3_POOL_ABI)
        self.events_to_listen = ['Swap']

    async def set_initial_price(self):
        eth_usdt_contract = self.client.get_contract(
            contract_address=self.eth_usdt_pool_address, abi=UNISWAP_V3_POOL_ABI
            )
        eth_usdt_slot0_call = await eth_usdt_contract.functions.slot0().call()
        self.eth_usdt_price = await self.calculate_price_from_sqrtPriceX96(
            eth_usdt_slot0_call[0], self.usdt_decimals, 18
        )

        eth_dai_contract = self.client.get_contract(
            contract_address=self.eth_dai_pool_address, abi=UNISWAP_V3_POOL_ABI
            )
        eth_dai_slot0_call = await eth_dai_contract.functions.slot0().call()
        self.eth_dai_price = await self.calculate_price_from_sqrtPriceX96(
            eth_dai_slot0_call[0], self.dai_decimals, 18
        )
        
        logger.success(f'Initial prices from slot0 successfully set: '
                       f'ETH/USDT: {self.eth_usdt_price:.2f}, '
                       f'ETH/DAI: {self.eth_dai_price:.2f}')

    async def get_topics_from_events_and_abi(self):
        event_topic_mapping = {}
        try:
            for event_name in self.events_to_listen:
                event = getattr(self.pool_contract.events, event_name)()
                topic = self.client.w3.to_hex(event_abi_to_log_topic(event.abi))
                event_topic_mapping[event_name] = topic
        except Exception as error:
            raise RuntimeError(f'Error getting topics from ABI: {error}')

        logger.success(f'Topics {self.events_to_listen} successfully mapped:')
        for event_name, topic in event_topic_mapping.items():
            logger.success(f'Event: {event_name} -> Topic: {topic}')
        
        self.event_topic_mapping = event_topic_mapping

        return list(event_topic_mapping.values())

    async def decode_event_result(self, result):
        topic_signature = self.client.w3.to_hex(result['topics'][0])
        for name, topic in self.event_topic_mapping.items():
            if topic == topic_signature:
                event_name = name
                break
    
        decoded_data = getattr(self.pool_contract.events, event_name)().process_log(result)
        # logger.info(f"https://arbiscan.io/tx/{self.client.w3.to_hex(decoded_data['transactionHash'])}")
        # logger.info(json.dumps(dict(decoded_data['args']), indent=4))
        sqrt_price_x96 = decoded_data['args']['sqrtPriceX96']
        
        if result['address'] == self.eth_usdt_pool_address:
            price_eth_in_usdt = await self.calculate_price_from_sqrtPriceX96(sqrt_price_x96, self.usdt_decimals, 18)
            self.eth_usdt_price = price_eth_in_usdt
            logger.info(f'New event ETH/USDT: {price_eth_in_usdt:.2f}')
        if result['address'] == self.eth_dai_pool_address:
            price_eth_in_dai = await self.calculate_price_from_sqrtPriceX96(sqrt_price_x96, self.dai_decimals, 18)
            self.eth_dai_price = price_eth_in_dai
            logger.info(f'New event  ETH/DAI: {price_eth_in_dai:.2f}')
            
        await self.check_arbitrage_opportunity()

    async def calculate_price_from_sqrtPriceX96(
        self, sqrt_price_x96: int, decimals_token0: int, decimals_token1: int
        ) -> float:
        sqrt_price = sqrt_price_x96 / (2**96)   
        price = sqrt_price ** 2
        price_adjusted = price * (10 ** (decimals_token1 - decimals_token0))
        return price_adjusted

    async def check_arbitrage_opportunity(self) -> None:
        if self.eth_usdt_price > self.eth_dai_price:
            percentage_diff = (self.eth_usdt_price - self.eth_dai_price) / self.eth_dai_price * 100
            if percentage_diff > self.spread_percentage_threshold:
                logger.success(f'Arbitrage opportunity found: '
                               f'ETH/USDT {self.eth_usdt_price:.2f} --> ETH/DAI {self.eth_dai_price:.2f} '
                               f'({percentage_diff:.2f}%)')
        if self.eth_dai_price > self.eth_usdt_price:
            percentage_diff = (self.eth_dai_price - self.eth_usdt_price) / self.eth_usdt_price * 100
            if percentage_diff > self.spread_percentage_threshold:
                logger.success(f'Arbitrage opportunity found: '
                               f'ETH/DAI {self.eth_dai_price:.2f} --> ETH/USDT {self.eth_usdt_price:.2f} '
                               f'({percentage_diff:.2f}%)')

    async def monitor_pools(self) -> None:
        async with AsyncWeb3(WebSocketProvider(self.alchemy_wss_url)) as w3_wss:
            if (await w3_wss.is_connected()):
                logger.success(f'Successfully connected to WSS provider')

            topics = await self.get_topics_from_events_and_abi()
            subscription_args = {
                "address": [self.eth_usdt_pool_address, self.eth_dai_pool_address],
                'topics': [topics]
            }
            await w3_wss.eth.subscribe(
                    "logs",
                    subscription_args,
            )
            await self.set_initial_price()
            logger.info(f"Start monitoring spread threshold {self.spread_percentage_threshold}% in "
                        f"{[self.eth_usdt_pool_address, self.eth_dai_pool_address]} pools")

            try:
                async for response in w3_wss.socket.process_subscriptions():
                    result: AttributeDict = response.get("result")
                    if result:
                        await self.decode_event_result(result)

            except Exception as error:
                raise RuntimeError(f'Error in monitor_pool: {error}')
