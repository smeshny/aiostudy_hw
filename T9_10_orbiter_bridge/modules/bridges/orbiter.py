import asyncio
import json

from custom_logger import logger
from client import Client
from networks import get_network_by_name
from config import TOKENS_PER_CHAIN, ORBITER_V3_ABI


class Orbiter:
    def __init__(self, client: Client) -> None:
        self.client: Client = client
        self.native_token = self.client.network.token

    async def get_bridge_data(self, src_token_name: str, dst_token_name: str):
        url = "https://api.orbiter.finance/sdk/routers/v2"
        response = await self.client.make_request(method='GET', url=url)
        
        bridge_line = f"{src_token_name}/{dst_token_name}"
        # print(response)

        pass

    async def bridge(
        self, 
        src_token_name: str, 
        src_token_address: str,
        src_chain: str,
        dst_token_name: str, 
        dst_token_address: str, 
        dst_chain: str,
        amount_to_bridge_ether: float
        ):
        # await self.get_bridge_data(src_token_name, dst_token_name)
        print(dst_chain.chain_id)
        pass

