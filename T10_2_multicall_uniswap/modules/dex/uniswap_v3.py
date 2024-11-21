import asyncio
import time
import random
from dataclasses import dataclass

from eth_utils import to_canonical_address
from eth_account.messages import encode_typed_data

from client import Client
from custom_logger import logger
from modules.dex.odos import Odos
from modules.multicall_functions import Multicall3
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
        self.external_price_provider = Odos(client=self.client)
        self.multicall3 = Multicall3(client=self.client)
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
        
    # async def check_pool_and_return_fee(self, token_a_address: str, token_b_address: str) -> int:
    #     possible_fees: list[int] = [100, 500, 2000, 2500, 3000, 5000, 10000]
    #     for fee in possible_fees:
    #         # todo: makemulticall3 fetch
    #         pool_address = await self.factory_contract.functions.getPool(token_a_address, token_b_address, fee).call()
    #         if pool_address != ZERO_ADDRESS:
    #             return fee
    #     raise RuntimeError(f"Can't find pool for tokens {token_a_address} and {token_b_address}")
    
    async def check_pool_and_return_fee(self, token_a_address: str, token_b_address: str) -> int:
        possible_fees: list[int] = [100, 200, 300, 400, 500, 1000, 2000, 2500, 3000, 5000, 10000]
        
        fetched_pools_data = await self.multicall3.fetch_pools_data_from_factory(
            token_a_address, token_b_address, possible_fees, self.factory_contract)
    
    async def get_path(self, token_a_address: str, token_b_address: str) -> bytes:
        fee = await self.check_pool_and_return_fee(token_a_address, token_b_address)
        # Convert the token addresses to bytes
        token_a_bytes = to_canonical_address(token_a_address)
        token_b_bytes = to_canonical_address(token_b_address)
        path = token_a_bytes + fee.to_bytes(3, 'big') + token_b_bytes
        return path
    
    async def get_min_amount_out(
        self, 
        input_amount_wei: int, 
        token_a_name: str, token_a_address: str, 
        token_b_name: str, token_b_address: str, 
        slippage: float, 
        path: bytes
        ) -> int:
        uniswap_v3_quote = await self.quoter_contract.functions.quoteExactInput(path, input_amount_wei).call()
        uniswap_v3_amount_out = int(uniswap_v3_quote[0])
        min_amount_out_with_slippage = int(uniswap_v3_amount_out * (100 - slippage) / 100)
        
        external_quote = await self.external_price_provider.get_external_quote(
            input_token=token_a_address, output_token=token_b_address, input_amount=input_amount_wei, slippage=slippage
            )
        external_amount_out = int(external_quote['outAmounts'][0])
        difference_in_percentage = (external_amount_out - uniswap_v3_amount_out) / external_amount_out * 100
        token_pair_name = f"{token_a_name}/{token_b_name}"
        
        if difference_in_percentage > 0:
            logger.warning(f"ODOS quote for {token_pair_name} is better than Uniswap V3 quote by "
                           f"{difference_in_percentage:.1f}%")
        else:
            logger.warning(f"Uniswap V3 quote for {token_pair_name} is better than ODOS quote by "
                           f"{difference_in_percentage:.1f}%") 
        
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
            input_amount_wei, input_token_name, input_token, output_token_name, output_token, slippage, path
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

    async def make_one_multicall_erc20_spend_approval(self, tokens_to_approve: list[tuple[str, int]]):
        approval_calls = []
        # todo: make this asycnio gather
        for token_to_approve in tokens_to_approve:
            deadline = int(time.time()) + 360
            token_address, amount_in_wei = token_to_approve
            
            token_params_multicall = await self.multicall3.get_erc20_token_parameters_for_permit(token_address)
            token_name_from_contract, token_version, token_erc20_nonce = token_params_multicall
            
            # Define the EIP-712 domain
            domain = {
                "name": token_name_from_contract,
                "version": token_version,
                "chainId": self.client.network.chain_id,
                "verifyingContract": token_address
            }
            
            # Define the Permit type
            permit_type = {
                "Permit": [
                    {"name": "owner", "type": "address"},
                    {"name": "spender", "type": "address"},
                    {"name": "value", "type": "uint256"},
                    {"name": "nonce", "type": "uint256"},
                    {"name": "deadline", "type": "uint256"},
                ]
            }

            # Construct the permit message
            message = {
                "types": {
                    "EIP712Domain": [
                        {"name": "name", "type": "string"},
                        {"name": "version", "type": "string"},
                        {"name": "chainId", "type": "uint256"},
                        {"name": "verifyingContract", "type": "address"},
                    ],
                    **permit_type
                },
                "domain": domain,
                "primaryType": "Permit",
                "message": {
                    "owner": self.client.address,
                    "spender": self.router_address,
                    "value": amount_in_wei,
                    "nonce": token_erc20_nonce,
                    "deadline": deadline,
                },
            }
            
            signable_message = encode_typed_data(full_message=message)
            # sign message:
            signed_message = self.client.w3.eth.account.sign_message(
                signable_message=signable_message, private_key=self.client.private_key
                )
            v, r, s = signed_message.v, signed_message.r, signed_message.s
            r_bytes = r.to_bytes(32, byteorder='big')
            s_bytes = s.to_bytes(32, byteorder='big')
            
            # selfPermitIfNecessary only call if allowance is insufficient
            erc20_approve_call = self.router_contract.encode_abi(
                abi_element_identifier='selfPermitIfNecessary',
                args=[
                    token_address, 
                    amount_in_wei, 
                    deadline, 
                    v, 
                    r_bytes, 
                    s_bytes]
                )
            approval_calls.append(erc20_approve_call)
            
        try:
            tx_params = (await self.client.prepare_transaction()) | {
                'value': 0,
            }
            transaction = await self.router_contract.functions.multicall(
                approval_calls,
            ).build_transaction(tx_params)
            return await self.client.send_transaction(transaction)
        except Exception as error:
            raise error


    async def multicall_swap(
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
        
        if self.native_token in all_from_token_names or self.native_token in all_to_token_names:
            tx_additional_data = self.router_contract.encode_abi(
                abi_element_identifier='unwrapWETH9' if self.native_token not in all_from_token_names else 'refundETH',
                args=[
                    min_amount_out_wei,
                    self.client.address
                ] if self.native_token not in all_from_token_names else None
            )
            all_multicall_data.append(tx_additional_data)
        
        logger.info(f"All data fetched, start perfoming steps for swap on Uniswap V3...")
        
        if all_tokens_to_approve:
            logger.info(f"Start batch multicall approve for {len(all_tokens_to_approve)} tokens")
            await self.make_one_multicall_erc20_spend_approval(all_tokens_to_approve)
        
        #########################################################################################
        # this approach is not working because msg.sender is multicall3 contract address
        # if all_tokens_to_approve:
        #     await self.multicall3.make_multiple_erc20_spend_approvals(all_tokens_to_approve)
        #########################################################################################

        logger.info(f"Start multicall swap on Uniswap V3...")
        
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
                raise RuntimeError(f"Probably you don't have enough tokens for this swap! Error: {error}")
            else:
                raise error
