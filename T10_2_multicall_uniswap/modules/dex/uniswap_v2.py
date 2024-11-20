import asyncio
import time

from client import Client
from config import TOKENS_PER_CHAIN, CONTRACTS_PER_CHAIN, UNISWAP_V2_FACTORY_ABI, UNISWAP_V2_ROUTER_ABI
from modules.dex.odos import Odos


class UniswapV2:
    def __init__(self, client: Client) -> None:
        self.client: Client = client
        self.native_token = self.client.network.token
        self.router_address = CONTRACTS_PER_CHAIN[self.client.network.name]["UNISWAP_V2_ROUTER"]
        self.factory_address = CONTRACTS_PER_CHAIN[self.client.network.name]["UNISWAP_V2_FACTORY"]
        self.router_contract = self.client.get_contract(
            contract_address=self.router_address, abi=UNISWAP_V2_ROUTER_ABI
            )
        # self.factory_contract = self.client.get_contract(
        #     contract_address=self.factory_address, abi=UNISWAP_V2_FACTORY_ABI
        #     )
        self.external_price_provider = Odos(client=self.client)
    
    # async def get_pair_address(self, token_a: str, token_b: str) -> str:
    #     pair_address = await self.factory_contract.functions.getPair(token_a, token_b).call()
    #     return pair_address
    
    async def get_min_amount_out(self, input_amount_wei: int, token_a: str, token_b: str, slippage: float) -> int:
        uniswap_v2_quote = await self.router_contract.functions.getAmountsOut(input_amount_wei, [token_a, token_b]).call()
        uniswap_v2_amount_out = int(uniswap_v2_quote[1])
        min_amount_out_with_slippage = int(uniswap_v2_amount_out * (100 - slippage) / 100)
        
        # Print if the external quote is better than the Uniswap V2 quote
        external_quote = await self.external_price_provider.get_external_quote(
            input_token=token_a, output_token=token_b, input_amount=input_amount_wei, slippage=slippage
            )
        external_amount_out = int(external_quote['outAmounts'][0])
        difference_in_percentage = (external_amount_out - uniswap_v2_amount_out) / external_amount_out * 100
        
        if difference_in_percentage > 0:
            print(f"ODOS quote is better than Uniswap V2 quote by {difference_in_percentage:.1f}%")
        else:
            print(f"Uniswap V2 quote is better than ODOS quote by {difference_in_percentage:.1f}%") 
        
        return min_amount_out_with_slippage
    
    async def swap(self, input_token: str, input_token_name: str, output_token: str, 
                   output_token_name: str, input_amount: float, slippage: float
                   ):
        decimals_input_token = await self.client.get_decimals(token_address=input_token)
        input_amount_wei = self.client.to_wei(input_amount, decimals=decimals_input_token)

        min_amount_out_wei = await self.get_min_amount_out(input_amount_wei, input_token, output_token, slippage)
    
        decimals_output_token = await self.client.get_decimals(token_address=output_token)
        min_amount_out_ether = self.client.from_wei(min_amount_out_wei, decimals=decimals_output_token)
        
        if input_token_name == self.native_token:
            swap_function = self.router_contract.functions.swapExactETHForTokens
            value = input_amount_wei
        elif output_token_name == self.native_token:
            swap_function = self.router_contract.functions.swapExactTokensForETH
            value = 0
        else:
            swap_function = self.router_contract.functions.swapExactTokensForTokens
            value = 0

        deadline = int(time.time() + 60 * 12)
        
        print(f"Start swap on Uniswap V2: {input_amount:.6f} {input_token_name} -> "
              f"{min_amount_out_ether:.6f} {output_token_name}"
        )
        
        if input_token_name != self.native_token:
            await self.client.check_for_approved(
                token_address=input_token, spender_address=self.router_address, amount_in_wei=input_amount_wei
                )
        
        try:
            tx_params = (await self.client.prepare_transaction()) | {
                'value': value,
            }
            
            transaction = await swap_function(
                *([input_amount_wei] if input_token_name != self.native_token else []), 
                min_amount_out_wei, 
                [input_token, output_token], 
                self.client.address, 
                deadline
                ).build_transaction(tx_params)
            
            return await self.client.send_transaction(transaction)
        except Exception as error:
            if 'TRANSFER_FROM_FAILED' in str(error):
                raise RuntimeError(f"You don't have enough {input_token_name} for this swap")
            if 'insufficient funds for transfer' in str(error):
                raise RuntimeError(f"You don't have enough {self.native_token} for this swap")
            else:
                raise error