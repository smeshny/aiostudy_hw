import asyncio
import time
from dataclasses import dataclass

from eth_utils import to_canonical_address

from client import Client
from custom_logger import logger
from modules.dex.odos import Odos
from config import (TOKENS_PER_CHAIN, CONTRACTS_PER_CHAIN, UNISWAP_V3_ROUTER_02_ABI, UNISWAP_V3_QUOTER_V2_ABI,
                    UNISWAP_V3_FACTORY_ABI, ZERO_ADDRESS
                    )


@dataclass
class SwapPair:
    from_token_name: str
    to_token_name: str
    from_amount: float
    slippage: float


class UniswapV3:
    def __init__(self, client: Client) -> None:
        self.client: Client = client
        self.native_token = self.client.network.token
        self.router_address = CONTRACTS_PER_CHAIN[self.client.network.name]["UNISWAP_V3_ROUTER_02"]
        self.router_contract = self.client.get_contract(
            contract_address=self.router_address, abi=UNISWAP_V3_ROUTER_02_ABI
            )
        self.quoter_address = CONTRACTS_PER_CHAIN[self.client.network.name]["UNISWAP_V3_QUOTER_V2"]
        self.quoter_contract = self.client.get_contract(
            contract_address=self.quoter_address, abi=UNISWAP_V3_QUOTER_V2_ABI
            )
        self.factory_address = CONTRACTS_PER_CHAIN[self.client.network.name]["UNISWAP_V3_FACTORY"]
        self.factory_contract = self.client.get_contract(
            contract_address=self.factory_address, abi=UNISWAP_V3_FACTORY_ABI
            )
        self.external_price_provider = Odos(client=self.client)
        
    async def check_pool_and_return_fee(self, token_a_address: str, token_b_address: str) -> int:
        possible_fees: list[int] = [100, 500, 2000, 2500, 3000, 5000, 10000]
        for fee in possible_fees:
            pool_address = await self.factory_contract.functions.getPool(token_a_address, token_b_address, fee).call()
            if pool_address != ZERO_ADDRESS:
                return fee
        raise RuntimeError(f"Can't find pool for tokens {token_a_address} and {token_b_address}")
    
    async def get_path(self, token_a_address: str, token_b_address: str) -> bytes:
        fee = await self.check_pool_and_return_fee(token_a_address, token_b_address)
        # Convert the token addresses to bytes
        token_a_bytes = to_canonical_address(token_a_address)
        token_b_bytes = to_canonical_address(token_b_address)
        path = token_a_bytes + fee.to_bytes(3, 'big') + token_b_bytes
        return path
    
    async def get_min_amount_out(
        self, input_amount_wei: int, token_a_address: str, token_b_address: str, slippage: float, path: bytes
        ) -> int:
        uniswap_v3_quote = await self.quoter_contract.functions.quoteExactInput(path, input_amount_wei).call()
        uniswap_v3_amount_out = int(uniswap_v3_quote[0])
        min_amount_out_with_slippage = int(uniswap_v3_amount_out * (100 - slippage) / 100)
        
        # Print if the external quote is better than the Uniswap V3 quote
        external_quote = await self.external_price_provider.get_external_quote(
            input_token=token_a_address, output_token=token_b_address, input_amount=input_amount_wei, slippage=slippage
            )
        external_amount_out = int(external_quote['outAmounts'][0])
        difference_in_percentage = (external_amount_out - uniswap_v3_amount_out) / external_amount_out * 100
        
        if difference_in_percentage > 0:
            logger.warning(f"ODOS quote is better than Uniswap V3 quote by {difference_in_percentage:.1f}%")
        else:
            logger.warning(f"Uniswap V3 quote is better than ODOS quote by {difference_in_percentage:.1f}%") 
        
        return min_amount_out_with_slippage
    
    async def get_multicall_params_for_swap(
        self, 
        input_token_name: str,
        output_token_name: str, 
        input_amount: float, 
        slippage: float
        ):
        if input_token_name in ('ETH', 'WETH', 'BNB', 'WBNB') and output_token_name in ('ETH', 'WETH', 'BNB', 'WBNB'):
            raise RuntimeError(
                "Sorry, you can't swap ETH->WETH or WETH->ETH, because it's not a swap, it's wrap or unwrap"
                )
            
        input_token = TOKENS_PER_CHAIN[self.client.network.name][input_token_name]
        output_token = TOKENS_PER_CHAIN[self.client.network.name][output_token_name]
        
        decimals_input_token = await self.client.get_decimals(token_address=input_token)
        input_amount_wei = self.client.to_wei(input_amount, decimals=decimals_input_token)
        
        if input_amount == 0:
            if input_token_name == self.native_token:
                native_balance = await self.client.w3.eth.get_balance(self.client.address)
                raise RuntimeError(f"Sorry, You can't swap all balance of native token! "
                                   f"Your balance is {self.client.from_wei(native_balance):.6f} {input_token_name}"
                                   )
            else:
                input_amount_wei = await self.client.get_erc20_balance(token_address=input_token)
                input_amount = self.client.from_wei(input_amount_wei, decimals=decimals_input_token)

        path: bytes = await self.get_path(input_token, output_token)
        min_amount_out_wei: int = await self.get_min_amount_out(
            input_amount_wei, input_token, output_token, slippage, path
            )
    
        decimals_output_token = await self.client.get_decimals(token_address=output_token)
        min_amount_out_ether = self.client.from_wei(min_amount_out_wei, decimals=decimals_output_token)
        
        multicall_data = []
        
        swap_data = self.router_contract.encode_abi(
            abi_element_identifier='exactInput',
            args=[{
                'path': path,
                'recipient': self.client.address if output_token_name != self.native_token
                else self.router_address,
                'amountIn': input_amount_wei,
                'amountOutMinimum': min_amount_out_wei
            }]
        )
        multicall_data.append(swap_data)
        
        value_wei = input_amount_wei if input_token_name == self.native_token else 0
        min_amount_out_native_wei = min_amount_out_wei if output_token_name == self.native_token else 0
        
        tokens_to_approve = []
        if input_token_name != self.native_token:
            tokens_to_approve.append((input_token, input_amount_wei))
        
        logger.info(f"Successfully fetched data for swap on Uniswap V3: {input_amount:.6f} {input_token_name} -> "
              f"{min_amount_out_ether:.6f} {output_token_name}"
        )
        
        return multicall_data, value_wei, min_amount_out_native_wei, tokens_to_approve

    async def multicallswap(
        self,
        swap_pairs: list[SwapPair]
        ):
        all_multicall_data = []
        total_value_wei = 0
        min_amount_out_wei = 0
        all_tokens_to_approve = []
        all_from_token_names = [swap_pair.from_token_name for swap_pair in swap_pairs]
        all_to_token_names = [swap_pair.to_token_name for swap_pair in swap_pairs]
        
        multicall_params_responses = await asyncio.gather(*[
            self.get_multicall_params_for_swap(
                swap_pair.from_token_name,
                swap_pair.to_token_name,
                swap_pair.from_amount,
                swap_pair.slippage
            )
            for swap_pair in swap_pairs
        ])
        
        for multicall_data, value_wei, min_amount_out_native_wei, token_to_approve in multicall_params_responses:
            all_multicall_data.extend(multicall_data)
            total_value_wei += value_wei
            min_amount_out_wei += min_amount_out_native_wei
            all_tokens_to_approve.extend(token_to_approve)
        
        logger.info(f"Start perfoming multicall swap on Uniswap V3...")
        
        if self.native_token in all_from_token_names or self.native_token in all_to_token_names:
            tx_additional_data = self.router_contract.encode_abi(
                abi_element_identifier='unwrapWETH9' if self.native_token not in all_from_token_names else 'refundETH',
                args=[
                    min_amount_out_wei,
                    self.client.address
                ] if self.native_token not in all_from_token_names else None
            )
            all_multicall_data.append(tx_additional_data)
            
        for token_to_approve in all_tokens_to_approve:
            await self.client.check_for_approved(
                token_address=token_to_approve[0], 
                spender_address=self.router_address, 
                amount_in_wei=token_to_approve[1]
                )
            
        try:
            tx_params = (await self.client.prepare_transaction()) | {
                'value': total_value_wei,
            }
  
            transaction = await self.router_contract.functions.multicall(
                all_multicall_data,
            ).build_transaction(tx_params)
            return await self.client.send_transaction(transaction)
        except Exception as error:
            if 'execution reverted: STF' in str(error):
                raise RuntimeError(f"Probably you don't have enough tokens for this swap: {error}")
            else:
                raise error
