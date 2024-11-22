import asyncio
import time
import random
import json

from web3 import AsyncWeb3, WebSocketProvider
from web3.datastructures import AttributeDict
from web3._utils.events import event_abi_to_log_topic

from client import Client
from custom_logger import logger
from config import UNISWAP_V3_POOL_ABI


class UniswapMevBot:
    def __init__(self, client: Client, wss_provider: str, pool_address: str, events_to_listen: list[str]):
        self.client = client
        self.alchemy_wss_url = wss_provider
        self.pool_address = pool_address
        self.pool_contract = self.client.get_contract(abi=UNISWAP_V3_POOL_ABI)
        self.events_to_listen = events_to_listen

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
        
        logger.success(f'Found new event: {event_name}')
        decoded_data = getattr(self.pool_contract.events, event_name)().process_log(result)
        logger.info(f"https://arbiscan.io/tx/{self.client.w3.to_hex(decoded_data['transactionHash'])}")
        logger.info(json.dumps(dict(decoded_data['args']), indent=4))

    async def monitor_pool(self):
        async with AsyncWeb3(WebSocketProvider(self.alchemy_wss_url)) as w3_wss:
            if (await w3_wss.is_connected()):
                logger.success(f'Successfully connected to WSS provider')

            topics = await self.get_topics_from_events_and_abi()
            subscription_args = {
                "address": self.pool_address,
                'topics': [topics]
            }
            await w3_wss.eth.subscribe(
                    "logs",
                    subscription_args,
            )
            
            logger.info(f'Start monitoring {self.pool_address} pool')
            try:
                async for response in w3_wss.socket.process_subscriptions():
                    result: AttributeDict = response.get("result")
                    if result:
                        await self.decode_event_result(result)

            except Exception as error:
                raise RuntimeError(f'Error in monitor_pool: {error}')
