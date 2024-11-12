import asyncio
import time

from eth_utils import to_canonical_address

from client import Client
from modules.dex.odos import Odos
from config import (CONTRACTS_PER_CHAIN, IZUMI_SWAP_ROUTER_ABI, IZUMI_QUOTER_ABI,
                    IZUMI_FACTORY_ABI, ZERO_ADDRESS
                    )


class Izumi:
    def __init__(self, client: Client) -> None:
        self.client: Client = client
        self.native_token = self.client.network.token
        self.router_address = CONTRACTS_PER_CHAIN[self.client.network.name]["IZUMI_SWAP_ROUTER"]
        self.router_contract = self.client.get_contract(
            contract_address=self.router_address, abi=IZUMI_SWAP_ROUTER_ABI
            )
        self.quoter_address = CONTRACTS_PER_CHAIN[self.client.network.name]["IZUMI_QUOTER"]
        self.quoter_contract = self.client.get_contract(
            contract_address=self.quoter_address, abi=IZUMI_QUOTER_ABI
            )
        self.factory_address = CONTRACTS_PER_CHAIN[self.client.network.name]["IZUMI_FACTORY"]
        self.factory_contract = self.client.get_contract(
            contract_address=self.factory_address, abi=IZUMI_FACTORY_ABI
            )
        self.external_price_provider = Odos(client=self.client)
    
    async def check_pool_and_return_fee(self, token_a: str, token_b: str) -> tuple[str, int]:
        possible_fees: list[int] = [100, 400, 500, 2000, 2500, 3000, 5000, 10000]
        for fee in possible_fees:
            pool_address = await self.factory_contract.functions.pool(token_a, token_b, fee).call()
            if pool_address != ZERO_ADDRESS:
                return fee
        raise RuntimeError(f"Can't find pool for tokens {token_a} and {token_b}")
    
    async def get_path(self, token_a: str, token_b: str) -> bytes:
        fee = await self.check_pool_and_return_fee(token_a, token_b)
        # Convert the token addresses to bytes
        token_a_bytes = to_canonical_address(token_a)
        token_b_bytes = to_canonical_address(token_b)
        path = token_a_bytes + fee.to_bytes(3, 'big') + token_b_bytes
        return path
    
    async def get_min_amount_out(
        self, input_amount_wei: int, token_a: str, token_b: str, slippage: float, path: bytes
        ) -> int:
        pancake_v3_quote = await self.quoter_contract.functions.swapAmount(input_amount_wei, path).call()
        pancake_v3_amount_out = int(pancake_v3_quote[0])
        min_amount_out_with_slippage = int(pancake_v3_amount_out * (100 - slippage) / 100)
        
        external_quote = await self.external_price_provider.get_external_quote(
            input_token=token_a, output_token=token_b, input_amount=input_amount_wei, slippage=slippage
            )
        external_amount_out = int(external_quote['outAmounts'][0])
        difference_in_percentage = (external_amount_out - pancake_v3_amount_out) / external_amount_out * 100
        
        # Protection for user money. Check if the external quote is better than the Izumi V3 quote
        if difference_in_percentage > 0:
            print(f"ODOS quote is better than Izumi V3 quote by {difference_in_percentage:.1f}%")
            if difference_in_percentage > 5:
                raise RuntimeError(f"ODOS quote is better than Izumi V3 quote by {difference_in_percentage:.1f}%. "
                                   f"Probably you will loose a lot of money!"
                                   )
        else:
            print(f"Izumi V3 quote is better than ODOS quote by {difference_in_percentage:.1f}%") 
        
        return min_amount_out_with_slippage
    
    async def swap(self, input_token: str, input_token_name: str, output_token: str, 
                   output_token_name: str, input_amount: float, slippage: float
                   ):
        if input_token_name in ('ETH', 'WETH', 'BNB', 'WBNB') and output_token_name in ('ETH', 'WETH', 'BNB', 'WBNB'):
            raise RuntimeError(
                "Sorry, you can't swap ETH->WETH or WETH->ETH, because it's not a swap, it's wrap or unwrap"
                )
        
        decimals_input_token = await self.client.get_decimals(token_address=input_token)
        input_amount_wei = self.client.to_wei(input_amount, decimals=decimals_input_token)
        
        if input_token_name == self.native_token:
            wallet_balance_wei = await self.client.w3.eth.get_balance(self.client.address)
        else:
            wallet_balance_wei = await self.client.get_erc20_balance(token_address=input_token)
            
        if wallet_balance_wei < input_amount_wei:
            raise RuntimeError(f"Sorry, you don't have enough {input_token_name} in your wallet")
            
        if input_amount == 0:
            if input_token_name == self.native_token:
                native_balance = await self.client.w3.eth.get_balance(self.client.address)
                raise RuntimeError(f"Sorry, You can't swap all balance of native token! "
                                   f"Your balance is {self.client.from_wei(native_balance):.6f} {input_token_name}"
                                   )
            else:
                input_amount_wei = await self.client.get_erc20_balance(token_address=input_token)
                if input_amount_wei == 0:
                    raise RuntimeError(f"Sorry, you don't have {input_token_name} in your wallet")
                input_amount = self.client.from_wei(input_amount_wei, decimals=decimals_input_token)

        path: bytes = await self.get_path(input_token, output_token)
        min_amount_out_wei: int = await self.get_min_amount_out(
            input_amount_wei, input_token, output_token, slippage, path
            )

        decimals_output_token = await self.client.get_decimals(token_address=output_token)
        min_amount_out_ether = self.client.from_wei(min_amount_out_wei, decimals=decimals_output_token)

        print(f"Start swap on Izumi V3 in {self.client.network.name} network: {input_amount:.6f} {input_token_name} -> "
              f"{min_amount_out_ether:.6f} {output_token_name}"
        )
        
        multicall_data = []
        deadline = int(time.time() + 60 * 12)
        
        swap_data = self.router_contract.encode_abi(
            abi_element_identifier='swapAmount',
            args=[{
                'path': path,
                'recipient': self.client.address if output_token_name != self.native_token
                else ZERO_ADDRESS,
                'amount': input_amount_wei,
                'minAcquired': min_amount_out_wei,
                'deadline': deadline,
            }]
        )
        multicall_data.append(swap_data)
        
        if output_token_name == self.native_token or input_token_name == self.native_token:
            tx_additional_data = self.router_contract.encode_abi(
                abi_element_identifier='unwrapWETH9' if input_token_name != self.native_token else 'refundETH',
                args=[
                    min_amount_out_wei,
                    self.client.address
                ] if input_token_name != self.native_token else None
            )
            multicall_data.append(tx_additional_data)
        
        if input_token_name != self.native_token:
            await self.client.check_for_approved(
                token_address=input_token, spender_address=self.router_address, amount_in_wei=input_amount_wei
                )
            
        try:
            tx_params = (await self.client.prepare_transaction()) | {
                'value': input_amount_wei if input_token_name == self.native_token else 0,
            }
  
            transaction = await self.router_contract.functions.multicall(
                multicall_data,
            ).build_transaction(tx_params)
            return await self.client.send_transaction(transaction)
        except Exception as error:
            if 'execution reverted: STF' in str(error):
                raise RuntimeError(f"Sorry, probably you don't have enough {input_token_name} for this swap")
            else:
                raise error