import asyncio
import json
import time
from collections import defaultdict

import eth_abi
from web3.contract import AsyncContract

from custom_logger import logger
from client import Client
from config import TOKENS_PER_CHAIN, CONTRACTS_PER_CHAIN, MULTICALL3_ABI


class Multicall3:
    def __init__(self, client: Client) -> None:
        self.client: Client = client
        self.native_token = self.client.network.token
        self.multicall3_address = CONTRACTS_PER_CHAIN[self.client.network.name]["MULTICALL3"]
        self.multicall3_contract = self.client.get_contract(
            contract_address=self.multicall3_address, abi=MULTICALL3_ABI
            )

    async def get_balances(self, tokens_to_check: list[str], wallets_to_check: list[str]):
        start_time = time.perf_counter()
        
        token_data = []
        for token_name in tokens_to_check:
            token_info = {
                'token_name': token_name,
                'token_address': TOKENS_PER_CHAIN[self.client.network.name][token_name]
            }
            token_data.append(token_info)

        wallets_to_check_checksum = [self.client.w3.to_checksum_address(wallet) for wallet in wallets_to_check]

        wallets_stats_primitive = []
        balance_calls = []
        for wallet in wallets_to_check_checksum:
            native_balance_call = self.multicall3_contract.encode_abi(
                abi_element_identifier='getEthBalance',
                args=[wallet]
            )
            balance_calls.append([self.multicall3_address, False, native_balance_call])
            wallets_stats_primitive.append([{
                'wallet': wallet,
                'native_balance': True,
            }])
            
            for token in token_data:
                token_contract = self.client.get_contract(contract_address=token['token_address'])
                erc20_balance_call = token_contract.encode_abi(
                    abi_element_identifier='balanceOf',
                    args=[wallet]
                )
                balance_calls.append([token['token_address'], False, erc20_balance_call])
                wallets_stats_primitive.append([{
                    'wallet': wallet,
                    'token_name': token['token_name'],
                    'token_balance': True,
                }])
                
                erc20_decimals_call = token_contract.encode_abi(
                    abi_element_identifier='decimals'
                )
                balance_calls.append([token['token_address'], False, erc20_decimals_call])
                wallets_stats_primitive.append([{
                    'wallet': wallet,
                    'token_name': token['token_name'],
                    'token_decimals': True,
                }])
        
        try:
            multicall_response = await self.multicall3_contract.functions.aggregate3(balance_calls).call()
        except Exception as error:
            if 'Request Entity Too Large' in str(error):
                raise RuntimeError(f'Try to reduce quantity of wallets to check')
            raise RuntimeError(f'Error during multicall: {error}')
        
        wallets_stats = defaultdict(dict)
        for i, (success, result) in enumerate(multicall_response):
            if wallets_stats_primitive[i][0].get('native_balance'):
                wallet = wallets_stats_primitive[i][0].get('wallet')
                native_balance_wei = self.client.w3.to_int(result)
                native_balance_ether = self.client.from_wei(native_balance_wei)
                wallets_stats[wallet][self.native_token] = float(native_balance_ether)
                
            if wallets_stats_primitive[i][0].get('token_balance'):
                wallet = wallets_stats_primitive[i][0].get('wallet')
                erc20_balance_wei = self.client.w3.to_int(result)
                wallets_stats[wallet][wallets_stats_primitive[i][0].get('token_name')] = int(erc20_balance_wei)
                
            if wallets_stats_primitive[i][0].get('token_decimals'):
                wallet = wallets_stats_primitive[i][0].get('wallet')
                token_decimals = self.client.w3.to_int(result)
                erc20_balance_wei = wallets_stats[wallet][wallets_stats_primitive[i][0].get('token_name')]
                erc20_balance_ether = float(self.client.from_wei(erc20_balance_wei, token_decimals))
                wallets_stats[wallet][wallets_stats_primitive[i][0].get('token_name')] = erc20_balance_ether

        end_time = time.perf_counter()
        elapsed_time = end_time - start_time
        
        logger.success(f'Stats for {len(wallets_to_check)} wallets in {self.client.network.name} succesfully fetched:')
        logger.debug(f'Execution time: {elapsed_time:.2f} seconds')
        logger.info(json.dumps(wallets_stats, indent=4))

    async def get_erc20_token_parameters_for_permit(self, token_address: str):
        parameters_calls = []
        token_contract = self.client.get_contract(contract_address=token_address)
        
        erc20_name_call = token_contract.encode_abi(
            abi_element_identifier='name',
        )
        parameters_calls.append([token_address, False, erc20_name_call])
        
        erc_20_version_call = token_contract.encode_abi(
            abi_element_identifier='version',
        )
        parameters_calls.append([token_address, True, erc_20_version_call])
        
        erc20_nonce_call = token_contract.encode_abi(
            abi_element_identifier='nonces',
            args=[self.client.address]
        )
        parameters_calls.append([token_address, False, erc20_nonce_call])
        
        try:
            multicall3_response = await self.multicall3_contract.functions.aggregate3(parameters_calls).call()
        except Exception as error:
            raise RuntimeError(f'Error during multicall3 fetch erc20 token parameters for permit: {error}')
        
        token_name_from_contract = eth_abi.decode(['string'], multicall3_response[0][1])[0]

        if multicall3_response[1][0]:  # if success is True and token have version parameter in contract
            token_version = eth_abi.decode(['string'], multicall3_response[1][1])[0]
        else:
            token_version = "1"  # if token have no version parameter in contract -> set version to default "1"
            
        token_erc20_nonce = self.client.w3.to_int(multicall3_response[2][1])
        
        return token_name_from_contract, token_version, token_erc20_nonce
    
    async def fetch_pools_data_from_factory(
        self, token_a_address: str, token_b_address: str, possible_fees: list[int], factory_contract: AsyncContract
        ) -> list[tuple[str, int]]:
        fee_calls = []
        for fee in possible_fees:
            fee_call = factory_contract.encode_abi(
                abi_element_identifier='getPool',
                args=[token_a_address, token_b_address, fee]
            )
            fee_calls.append([factory_contract.address, False, fee_call])
        
        try:
            multicall3_response = await self.multicall3_contract.functions.aggregate3(fee_calls).call()
        except Exception as error:
            raise RuntimeError(f'Error during multicall3 fetch pools data from factory: {error}')
        
        pools_data: list[tuple[str, int]] = []
        for i, (success, pool_address) in enumerate(multicall3_response):
            raw_pool_address = eth_abi.decode(['address'], pool_address)[0]
            checksum_pool_address = self.client.w3.to_checksum_address(raw_pool_address)
            pools_data.append((checksum_pool_address, possible_fees[i]))
            
        return pools_data

    # async def make_multiple_erc20_spend_approvals(self, tokens_to_approve_data: list[tuple[str, str, int]]):
    # '''
    # This naive approach is not working becaouse msg.sender in this case is multicall3 contract address
    # But for erc20 approve for router address msg.sender should be our wallet address
    # more information about msg.sender:
    
    
    # For this purpose UniswapV3Router contract has a functions *SelfPermit:
    # https://arbiscan.io/address/0x68b3465833fb72a70ecdf485e0e4c7bd8665fc45#writeProxyContract
    # '''
    
    
    #     multicall_approval_data = []
    #     for token_to_approve in tokens_to_approve_data:
    #         token_address, spender_address, amount_in_wei = token_to_approve
            
    #         erc20_approve_call = self.client.get_contract(contract_address=token_address).encode_abi(
    #             abi_element_identifier='approve',
    #             args=[spender_address, amount_in_wei]
    #         )
    #         multicall_approval_data.append([token_address, False, erc20_approve_call])
    #     logger.info(f"Performing multicall3 spend approvals for {len(tokens_to_approve_data)} tokens...")
    #     try:
    #         tx_params = (await self.client.prepare_transaction()) | {
    #             'value': 0,
    #         }
    #         transaction = await self.multicall3_contract.functions.aggregate3(
    #             multicall_approval_data
    #         ).build_transaction(tx_params)
    #         return await self.client.send_transaction(transaction)
    #     except Exception as error:
    #         raise RuntimeError(f'Error during multicall: {error}')
