import asyncio
import time

from eth_abi import abi

from custom_logger import logger
from client import Client
from config import TOKENS_PER_CHAIN, CONTRACTS_PER_CHAIN, ZERO_ADDRESS


class Multicall3:
    def __init__(self, client: Client) -> None:
        self.client: Client = client
        self.native_token = self.client.network.token
        self.router_address = CONTRACTS_PER_CHAIN[self.client.network.name]["SYNCSWAP_ROUTER_V2"]
        self.router_contract = self.client.get_contract(
            contract_address=self.router_address, abi=SYNCSWAP_ROUTER_V2_ABI
            )
        self.classic_factory_address = CONTRACTS_PER_CHAIN[self.client.network.name]["SYNCSWAP_CLASSIC_FACTORY"]
        self.classic_factory_contract = self.client.get_contract(
            contract_address=self.classic_factory_address, abi=SYNCSWAP_CLASSIC_FACTORY_ABI
        )