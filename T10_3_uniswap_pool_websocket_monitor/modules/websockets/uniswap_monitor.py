import asyncio
import time
import random
from dataclasses import dataclass

import web3
from web3 import AsyncWeb3, WebSocketProvider
from web3.datastructures import AttributeDict
from web3._utils.events import event_abi_to_log_topic


from client import Client
from custom_logger import logger
from config import (TOKENS_PER_CHAIN, CONTRACTS_PER_CHAIN, UNISWAP_V3_ROUTER_02_ABI, UNISWAP_V3_QUOTER_V2_ABI,
                    UNISWAP_V3_FACTORY_ABI, ZERO_ADDRESS , UNISWAP_V3_POOL_ABI
                    )


class UniswapMonitor:
    def __init__(self, client: Client, wss_provider: str, pool_address: str, events_to_listen: list[str]):
        self.client = client
        self.alchemy_wss_url = wss_provider
        self.pool_address = pool_address
        self.pool_contract = web3.AsyncWeb3().eth.contract(
            abi=UNISWAP_V3_POOL_ABI,
        )
        self.events_to_listen = events_to_listen

    async def get_topics_from_abi(self):
        event_topic_mapping = {}
        try:
            for event_name in self.events_to_listen:
                event = getattr(self.pool_contract.events, event_name)()
                topic = web3.Web3.to_hex(event_abi_to_log_topic(event.abi))
                event_topic_mapping[event_name] = topic
        except Exception as error:
            raise RuntimeError(f'Error getting topics from ABI: {error}')

        logger.success(f'Topics {self.events_to_listen} successfully mapped:')
        for event_name, topic in event_topic_mapping.items():
            logger.success(f'Event: {event_name} -> Topic: {topic}')
            
        return list(event_topic_mapping.values())
    
    async def decode_event_data(self, event_data: dict):
        pass

    async def monitor_pool(self):
        async with AsyncWeb3(WebSocketProvider(self.alchemy_wss_url)) as w3_wss:
            if (await w3_wss.is_connected()):
                logger.success(f'Successfully connected to WSS provider')
            
            topics = await self.get_topics_from_abi()
            await asyncio.sleep(1)
            subscription_args = {
                "address": self.pool_address,
                'topics': [topics]
            }
            await w3_wss.eth.subscribe(
                    "logs",
                    subscription_args,
            )
            try:
                async for response in w3_wss.socket.process_subscriptions():
                    logger.info(f"{response}\n")
                    # result: AttributeDict = event.get("result")
                    # if result:
                    #     transaction = result.get('transaction')
                    #     if transaction:
                    #         if transaction['from'] == FILTER_ADDRESS.lower():
                    #             print(f'Найдена транзакция с исходящим адресом: {FILTER_ADDRESS}')
                    #             tx_data = transaction.get('input')
                    #             if tx_data:
                    #                 print(f'Пробую декодировать входные данные: {tx_data}')
                    #                 decode_tx_data(tx_data)

            except Exception as error:
                print(f"Ошибка при прослушивании сокета: {error}")


# import asyncio
# import json
# import web3

# from web3 import AsyncWeb3, WebsocketProviderV2
# from web3.datastructures import AttributeDict


# with open('erc20_abi.json') as file:
#     ERC20_ABI = json.load(file)

# ALCHEMY_API_URL = "wss://arb-mainnet.g.alchemy.com/v2/pV_g26FmJVB3hNlhN5zPnfPdSIeb57HG"
# FILTER_ADDRESS = '0xd5a595d478b6de9B17a230F153551043823F8cc2'
# USDT_ADDRESS = "0xFd086bC7CD5C481DCC9C85ebE478A1C0b69FCbb9"


# def decode_tx_data(tx_data):
#     contract = web3.AsyncWeb3().eth.contract(
#         abi=ERC20_ABI
#     )

#     try:
#         function_abi = contract.decode_function_input(tx_data)
#         print(f'Успешно декодировал данные. Название функции: {function_abi[0]}, аргументы: {function_abi[1]}\n')
#     except Exception as error:
#         print(f'Не смог декодировать транзакцию: {error}\n')


# async def ws_v2_subscription_iterator():
#     async with AsyncWeb3.persistent_websocket(WebsocketProviderV2(ALCHEMY_API_URL)) as w3:

#         subscription_args = {
#             "addresses": [
#                 {
#                     "from": FILTER_ADDRESS,
#                 }
#             ],
#         }

#         subscription_id = await w3.eth.subscribe(
#             'alchemy_minedTransactions',  # type: ignore
#             subscription_args  # type: ignore
#         )

#         try:
#             async for event in w3.ws.process_subscriptions():
#                 print(event)
#                 result: AttributeDict = event.get("result")
#                 if result:
#                     transaction = result.get('transaction')
#                     if transaction:
#                         if transaction['from'] == FILTER_ADDRESS.lower():
#                             print(f'Найдена транзакция с исходящим адресом: {FILTER_ADDRESS}')
#                             tx_data = transaction.get('input')
#                             if tx_data:
#                                 print(f'Пробую декодировать входные данные: {tx_data}')
#                                 decode_tx_data(tx_data)

#         except Exception as error:
#             print(f"Ошибка при прослушивании сокета: {error}")

#         finally:
#             await w3.eth.unsubscribe(subscription_id)

# asyncio.run(ws_v2_subscription_iterator())