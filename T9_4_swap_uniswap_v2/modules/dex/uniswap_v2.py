import asyncio

from client import Client
from config import TOKENS_PER_CHAIN, CONTRACTS_PER_CHAIN, UNISWAP_V2_FACTORY_ABI, UNISWAP_V2_ROUTER_ABI
from modules.dex.odos import Odos


class UniswapV2:
    def __init__(self, client: Client) -> None:
        self.client: Client = client
        self.native_token = self.client.network.token
        self.router_address = CONTRACTS_PER_CHAIN[self.client.network.name]["UNISWAP_V2_ROUTER"]
        self.factory_address = CONTRACTS_PER_CHAIN[self.client.network.name]["UNISWAP_V2_FACTORY"]
        self.router_contract = self.client.get_contract(contract_address=self.router_address, abi=UNISWAP_V2_ROUTER_ABI)
        self.factory_contract = self.client.get_contract(contract_address=self.factory_address, abi=UNISWAP_V2_FACTORY_ABI)
        self.external_price_provider = Odos(client=self.client)
    
    async def get_pair_address(self, token_a: str, token_b: str) -> str:
        pair_address = await self.factory_contract.functions.getPair(token_a, token_b).call()
        return pair_address
    
    async def get_amounts_out(self, input_amount_wei: int, token_a: str, token_b: str, slippage: float) -> int:
        amount_out = await self.router_contract.functions.getAmountsOut(input_amount_wei, [token_a, token_b]).call()
        
        external_quote = await self.external_price_provider.get_external_quote(input_token=token_a, output_token=token_b, input_amount=input_amount_wei, slippage=slippage)
        external_amount_out = int(external_quote['outAmounts'][0])
        # external_amount_out = external_quote
        return amount_out[1], external_amount_out
    
    async def swap(self, input_token: str, input_token_name: str, output_token: str, 
                   output_token_name: str, input_amount: float, slippage: float
                   ):
        print(f"Pair address: {await self.get_pair_address(input_token, output_token)}")
        
        decimals_input_token = await self.client.get_decimals(token_address=input_token)
        input_amount_wei = self.client.to_wei(input_amount, decimals=decimals_input_token)
        
        print(f"Amounts out: {await self.get_amounts_out(input_amount_wei, input_token, output_token, slippage)}")
