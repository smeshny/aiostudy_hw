import asyncio

from client import Client
from config import TOKENS_PER_CHAIN


class XYfinance:
    def __init__(self, client: Client) -> None:
        self.client: Client = client
        self.base_url = "https://open-api.xy.finance/v1"
        self.native_token = self.client.network.token
        self.xy_native_token_address = "0xEeeeeEeeeEeEeeEeEeEeeEEEeeeeEeeeeeeeEEeE"
    
    async def get_swap_data(self, input_token: str, output_token: str, 
                            input_amount: int, slippage: int) -> dict:
        api_swap_url = self.base_url + '/swap'
        params = {
                "srcChainId": str(self.client.network.chain_id),
                "fromTokenAddress": input_token,
                "amount": str(input_amount),
                "destChainId": str(self.client.network.chain_id),
                "toTokenAddress": output_token,
                "receiveAddress": self.client.address,
                "slippage": str(slippage),
            }
            
        response = await self.client.make_request(
                method='GET',
                url=api_swap_url,
                headers={"Content-Type": "application/json"},
                params=params,
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
            input_token = self.xy_native_token_address
        if output_token == native_token_address:
            output_token = self.xy_native_token_address

        # get quote and call data for transaction
        xy_transaction = await self.get_swap_data(
            input_token, output_token, input_amount_wei, slippage
            )

        # if output token is zero address, set it to native token address
        if output_token == self.xy_native_token_address:
            output_token = native_token_address

        # get transaction amount details for logging
        output_value_wei = xy_transaction['toTokenAmount']
        decimals_output_token = await self.client.get_decimals(token_address=output_token)
        output_amount_ether = self.client.from_wei(output_value_wei, decimals=decimals_output_token)
        
        print(f"Start swap on XY.finance: {input_amount:.6f} {input_token_name} -> "
              f"{output_amount_ether:.6f} {output_token_name}"
        )
        
        value = int(xy_transaction['tx']['value'])
        spender_contract = xy_transaction['tx']['to']
        call_data = xy_transaction['tx']['data']
        
        if input_token != self.xy_native_token_address:
            await self.client.check_for_approved(input_token, spender_contract, input_amount_wei)

        try:
            tx_params = (await self.client.prepare_transaction()) | {
                'to': spender_contract,
                'value': value,
                'data': call_data,
            }
            return await self.client.send_transaction(tx_params)
        except Exception as error:
            if 'transfer amount exceeds balance' in str(error):
                raise RuntimeError(f"You don't have enough {input_token_name} for performing this swap")
            else:
                raise error