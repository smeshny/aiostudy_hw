import asyncio

from client import Client
from config import TOKENS_PER_CHAIN, ZERO_ADDRESS


class Odos:
    def __init__(self, client: Client) -> None:
        self.client: Client = client
        self.base_url = "https://api.odos.xyz/sor/"
        self.native_token = self.client.network.token
        
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
    
    async def get_external_quote(self, input_token: str, output_token: str, input_amount: int, slippage: int) -> dict:
        native_token_address = TOKENS_PER_CHAIN[self.client.network.name][self.client.network.token]
        
        # if native token, set it to zero address for odos
        if input_token == native_token_address:
            input_token = ZERO_ADDRESS
        if output_token == native_token_address:
            output_token = ZERO_ADDRESS
        
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
        
        return response    

    async def assemble(self, path_id: str) -> dict:
        assemble_url = self.base_url + 'assemble'
        assemble_request_body = {
            "userAddr": self.client.address,
            "pathId": path_id,
            "simulate": False, # this can be set to true if the user isn't doing their own estimate gas call for the transaction
        }
        
        response = await self.client.make_request(
            method='POST',
            url=assemble_url,
            headers={"Content-Type": "application/json"},
            json=assemble_request_body
        )
        
        return response

    async def swap(self, input_token: str, input_token_name: str, output_token: str, 
                   output_token_name: str, input_amount: int, slippage: float
                   ):
        
        native_token_address = TOKENS_PER_CHAIN[self.client.network.name][self.client.network.token]
        
        # get decimals and convert input amount from ether to wei
        decimals_input_token = await self.client.get_decimals(token_address=input_token)
        input_amount_wei = self.client.to_wei(input_amount, decimals=decimals_input_token)
        
        # if native token, set it to zero address for odos
        if input_token == native_token_address:
            input_token = ZERO_ADDRESS
        if output_token == native_token_address:
            output_token = ZERO_ADDRESS

        # get quote and call data for transaction
        path_id = await self.get_quote(input_token, output_token, input_amount_wei, slippage)
        odos_transaction = await self.assemble(path_id)

        # if output token is zero address, set it to native token address
        if output_token == ZERO_ADDRESS:
            output_token = native_token_address

        # get transaction amount details for logging
        output_value_wei = odos_transaction['outputTokens'][0]['amount']
        decimals_output_token = await self.client.get_decimals(token_address=output_token)
        output_amount_ether = self.client.from_wei(output_value_wei, decimals=decimals_output_token)
        
        
        print(f"Start swap on ODOS: {input_amount:.6f} {input_token_name} -> "
              f"{output_amount_ether:.6f} {output_token_name}"
        )
        
        value = int(odos_transaction['transaction']['value'])
        spender_odos_contract = odos_transaction['transaction']['to']
        call_data = odos_transaction['transaction']['data']
        
        if input_token != ZERO_ADDRESS:
            await self.client.check_for_approved(input_token, spender_odos_contract, input_amount_wei)

        try:
            tx_params = (await self.client.prepare_transaction()) | {
                'to': spender_odos_contract,
                'value': value,
                'data': call_data,
            }
            
            return await self.client.send_transaction(tx_params)
        except Exception as error:
            if 'transfer amount exceeds balance' in str(error):
                raise RuntimeError(f"You don't have enough {input_token_name} for performing this swap")
            else:
                raise error