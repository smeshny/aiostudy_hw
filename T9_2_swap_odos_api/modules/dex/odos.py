import asyncio

from eth_typing import HexStr

from client import Client
from config import TOKENS_PER_CHAIN
# from config import CONTRACTS_PER_CHAIN, ODOS_ABI


class Odos:
    def __init__(self, client: Client) -> None:
        self.client: Client = client
        self.base_url = "https://api.odos.xyz/sor/"
        # self.contract = self.client.w3.eth.contract(
        #     address=CONTRACTS_PER_CHAIN[self.client.network.name]['ODOS'],
        #     abi=ODOS_ABI
        # )
        
    async def get_quote(self, input_token: str, output_token: str, input_amount: int, slippage: int) -> dict:
        quote_url = self.base_url + 'quote/v2'
        quote_request_body = {
            "chainId": self.client.network.chain_id,
            "inputTokens": [
                {
                    "tokenAddress": input_token,
                    "amount": str(input_amount),
                }
            ],
            "outputTokens": [
                {
                    "tokenAddress": output_token,
                    "proportion": 1
                }
            ],
            "slippageLimitPercent": slippage, # set your slippage limit percentage (1 = 1%)
            "userAddr": self.client.address,
            "referralCode": 0,
            "disableRFQs": True,
            "compact": True,
        }
        
        response = await self.client.make_request(
            method='POST',
            url=quote_url,
            headers={"Content-Type": "application/json"},
            json=quote_request_body
        )
        
        return response['pathId']
    
    async def assemble(self, path_id: str) -> dict:
        assemble_url = self.base_url + 'assemble'
        assemble_request_body = {
            "userAddr": self.client.address, # the checksummed address used to generate the quote
            "pathId": path_id, # Replace with the pathId from quote response in step 1
            "simulate": False, # this can be set to true if the user isn't doing their own estimate gas call for the transaction
        }
        
        response = await self.client.make_request(
            method='POST',
            url=assemble_url,
            headers={"Content-Type": "application/json"},
            json=assemble_request_body
        )
        
        return response['transaction']['data']

    async def swap(self, input_token: str, output_token: str, input_amount: int, slippage: int):
        path_id = (await self.get_quote(input_token, output_token, input_amount, slippage))
        call_data = await self.assemble(path_id)
        print(call_data)