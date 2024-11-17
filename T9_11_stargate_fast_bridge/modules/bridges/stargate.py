import asyncio

from custom_logger import logger
from client import Client
from networks import Network
from config import TOKENS_PER_CHAIN, STARGATE_V2_ENDPOINT_ID, STARGATE_V2_POOLNATIVE_ABI, STARGATE_V2_POOLUSDC_ABI


class Stargate:
    def __init__(self, client: Client) -> None:
        self.client: Client = client
        self.native_token = self.client.network.token
        
    