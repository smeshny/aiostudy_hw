import asyncio
import json
from collections import defaultdict

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

        logger.success(f'Stats for {len(wallets_to_check)} wallets in {self.client.network.name} succesfully fetched:')
        logger.info(json.dumps(wallets_stats, indent=4))

