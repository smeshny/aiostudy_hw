import asyncio
import random

from aiohttp import ClientSession, TCPConnector
from aiohttp_socks import ProxyConnector

from web3 import AsyncHTTPProvider, AsyncWeb3
from web3.contract import AsyncContract
from web3.exceptions import TransactionNotFound
from eth_typing import HexStr

from networks import Network
from interfaces import BlockchainException
from config import ERC20_ABI, TOKENS_PER_CHAIN
from settings import GAS_PRICE_MULTIPLIER, GAS_LIMIT_MULTIPLIER, UNLIMITED_APPROVE


class Client:
    def __init__(
        self, 
        account_name: str | int, 
        network: Network, 
        private_key: None | str = None, 
        proxy: None | str = None
    ) -> None:
        
        self.network = network
        self.eip1559_support = network.eip1559_support
        self.token = network.token
        self.explorer = network.explorer
        self.chain_id = network.chain_id

        self.proxy_init = proxy
        self.request_kwargs = {"proxy": f"http://{proxy}", "ssl": False} if proxy else {"ssl": False}
        self.rpc = random.choice(network.rpc)
        self.w3 = AsyncWeb3(AsyncHTTPProvider(self.rpc, request_kwargs=self.request_kwargs))
        self.account_name = str(account_name)
        self.private_key = private_key if private_key else self.w3.eth.account.create().key.hex()
        self.address = AsyncWeb3.to_checksum_address(self.w3.eth.account.from_key(self.private_key).address)
        self.acc_info = account_name, self.address
        
    async def __aenter__(self):
        self.session: ClientSession = ClientSession(
            connector=ProxyConnector.from_url(f"http://{self.proxy_init}", ssl=False)
            if self.proxy_init else TCPConnector(ssl=False)
        )
        return self
    
    async def __aexit__(self, exc_type, exc_value, traceback) -> None:
        await self.session.close()
        
    async def make_request(self, method: str = 'GET', url: str = None, headers: dict = None, json: dict = None):
        async with self.session.request(method=method, url=url, headers=headers, json=json) as response:
            if response.status in [200, 201]:
                return await response.json()
            
            raise RuntimeError(f'{method} request failed with status {response.status}')

    async def get_decimals(self, token_name: str = None, token_address: str = None) -> int:
        contract_address = token_address if token_address else TOKENS_PER_CHAIN[self.network.name][token_name]
        contract = self.get_contract(contract_address)
        return await contract.functions.decimals().call()
    
    async def get_erc20_balance(self, token_name: str = None, token_address: str = None) -> int:
        contract_address = token_address if token_address else TOKENS_PER_CHAIN[self.network.name][token_name]
        contract = self.get_contract(contract_address)
        return await contract.functions.balanceOf(self.address).call()
    
    def get_contract(self, contract_address: str, abi: dict = ERC20_ABI) -> AsyncContract:
        return self.w3.eth.contract(
            address=AsyncWeb3.to_checksum_address(contract_address),
            abi=abi
        )
        
    async def get_allowance(self, token_address: str, spender_address: str) -> int:
        contract = self.get_contract(token_address)
        return await contract.functions.allowance(
            self.address,
            spender_address
        ).call()

    def to_wei(self, number: int | float | str, decimals: int = 18) -> int:

        unit_name = {
            18: 'ether',
            6: 'mwei'
        }[decimals]

        return self.w3.to_wei(number=number, unit=unit_name)

    async def check_for_approved(
            self, token_address: str, spender_address: str, amount_in_wei: int, 
            unlimited_approve: bool = UNLIMITED_APPROVE,
    ) -> bool:
        try:
            contract = self.get_contract(token_address)
            symbol = await contract.functions.symbol().call()

            print(f"Check for approval {symbol}")

            approved_amount_in_wei = await self.get_allowance(
                token_address=token_address,
                spender_address=spender_address
            )

            if amount_in_wei <= approved_amount_in_wei:
                print(f"Already approved")
                return False

            result = await self.make_approve(token_address, spender_address, amount_in_wei, unlimited_approve)

            await asyncio.sleep(random.randint(5, 9))
            
            return result
        except Exception as error:
            raise BlockchainException(f'{error}')
        
    async def make_approve(
            self, token_address: str, spender_address: str, amount_in_wei: int, unlimited_approve:bool
    ) -> bool:
        transaction = await self.get_contract(token_address).functions.approve(
            spender_address,
            amount=2 ** 256 - 1 if unlimited_approve else amount_in_wei
        ).build_transaction(await self.prepare_transaction())

        return await self.send_transaction(transaction)

    async def get_priority_fee(self) -> int:
        fee_history = await self.w3.eth.fee_history(5, 'latest', [20.0])
        non_empty_block_priority_fees = [fee[0] for fee in fee_history["reward"] if fee[0] != 0]

        divisor_priority = max(len(non_empty_block_priority_fees), 1)

        priority_fee = int(round(sum(non_empty_block_priority_fees) / divisor_priority))

        return priority_fee

    async def prepare_transaction(self, value: int = 0) -> dict:
        try:
            tx_params = {
                'chainId': self.network.chain_id,
                'from': self.w3.to_checksum_address(self.address),
                'nonce': await self.w3.eth.get_transaction_count(self.address),
                'value': value,
            }

            if self.network.eip1559_support:

                base_fee = await self.w3.eth.gas_price
                max_priority_fee_per_gas = await self.get_priority_fee()
                max_fee_per_gas = int(base_fee + max_priority_fee_per_gas * 1.05 * GAS_PRICE_MULTIPLIER)

                if self.network.name in ['Scroll', 'Optimism']:
                    max_fee_per_gas = int(max_fee_per_gas / GAS_PRICE_MULTIPLIER * 1.1)

                if max_priority_fee_per_gas > max_fee_per_gas:
                    max_priority_fee_per_gas = int(max_fee_per_gas * 0.95)

                tx_params['maxPriorityFeePerGas'] = max_priority_fee_per_gas
                tx_params['maxFeePerGas'] = int(max_fee_per_gas * 1.2)
                tx_params['type'] = '0x2'
            else:
                if self.network.name == 'BNB Chain':
                    tx_params['gasPrice'] = self.w3.to_wei(round(random.uniform(1.4, 1.5), 1), 'gwei')
                else:
                    gas_price = await self.w3.eth.gas_price
                    if self.network.name in ['Scroll', 'Optimism']:
                        gas_price = int(gas_price / GAS_PRICE_MULTIPLIER * 1.1)

                    tx_params['gasPrice'] = int(gas_price * 1.2 * GAS_PRICE_MULTIPLIER)

            return tx_params
        except Exception as error:
            raise BlockchainException(f'{error}')
        
    async def send_transaction(
            self, 
            transaction=None, 
            poll_latency: int = 10,
            timeout: int = 360, 
            signed_tx=None
    ) -> bool | HexStr:
        try:
            transaction['gas'] = int((await self.w3.eth.estimate_gas(transaction)) * GAS_LIMIT_MULTIPLIER)
        except Exception as error:
            raise BlockchainException(f'{error}')

        try:
            signed_tx = self.w3.eth.account.sign_transaction(transaction, self.private_key).raw_transaction
            tx_hash = self.w3.to_hex(await self.w3.eth.send_raw_transaction(signed_tx))
        except Exception as error:
            raise BlockchainException(f'{error}')

        total_time = 0
        while True:
            try:
                receipts = await self.w3.eth.get_transaction_receipt(tx_hash)
                status = receipts.get("status")
                if status == 1:
                    message = f'Transaction was successful: {self.explorer}tx/{tx_hash}'
                    print(message)
                    return True
                elif status is None:
                    await asyncio.sleep(poll_latency)
                else:
                    raise BlockchainException(f'Transaction failed: {self.explorer}tx/{tx_hash}')
            except TransactionNotFound:
                if total_time > timeout:
                    raise BlockchainException(f"Transaction is not in the chain after {timeout} seconds")
                total_time += poll_latency
                await asyncio.sleep(poll_latency)

            except Exception as error:
                if 'Transaction failed' in str(error):
                    raise BlockchainException(f'Transaction failed: {self.explorer}tx/{tx_hash}')
                print(f"Something went wrong. Error: {error}")
                total_time += poll_latency
                await asyncio.sleep(poll_latency)
                
    async def transfer_native_token(self, amount_to_transfer_eth: float, to_address: str) -> bool | HexStr:
        amount_to_transfer_in_wei = self.to_wei(amount_to_transfer_eth)
        to_address = self.w3.to_checksum_address(to_address)
        
        balance_wei = await self.w3.eth.get_balance(self.address)
        balance_in_eth = self.w3.from_wei(balance_wei, 'ether')
        print(f'Your balance is: {balance_in_eth:.8f} {self.network.token}')
        
        if balance_wei < amount_to_transfer_in_wei:
            raise Exception(f'You dont have enough {self.network.token} on your balance')

        print(f'Start to transfer {self.network.token} to {self.network.name} address '
              f'{to_address}: {amount_to_transfer_eth:.8f} {self.network.token}')

        try:
            tx_params = (await self.prepare_transaction()) | {
                'to': to_address,
                'value': amount_to_transfer_in_wei,
                'data': "0x"
            }

            return await self.send_transaction(tx_params)

        except Exception as error:
            print(f'{error}')
            
    async def transfer_erc20_token(
        self,
        token: str,
        amount_to_transfer_ether: float | None,
        to_address: str,
        ) -> bool | HexStr:
        
        to_address = self.w3.to_checksum_address(to_address)
        
        token_decimals = await self.get_decimals(token)
        token_address = TOKENS_PER_CHAIN[self.network.name][token]
        
        balance_wei = await self.get_erc20_balance(token)
        balance_in_ether = self.w3.from_wei(balance_wei, 'ether' if token_decimals == 18 else 'mwei')
        
        if not amount_to_transfer_ether:
            amount_to_transfer_in_wei = balance_wei
        else:
            amount_to_transfer_in_wei = self.to_wei(amount_to_transfer_ether, token_decimals)

        amount_to_transfer_ether = self.w3.from_wei(
            amount_to_transfer_in_wei, 'ether' if token_decimals == 18 else 'mwei'
            )
        print(f'Your {token} balance in {self.network.name} is: {balance_in_ether:.2f} {token}')
        
        if balance_wei < amount_to_transfer_in_wei:
            raise Exception(f'You dont have enough {token} to transfer on your balance')

        print(f'Start transfer {token} to {self.network.name} address '
              f'{to_address}: {amount_to_transfer_ether:.2f} {token}')

        await self.check_for_approved(
            token_address=token_address,
            spender_address=token_address,
            amount_in_wei=amount_to_transfer_in_wei)
        
        try:
            contract = self.get_contract(token_address)

            tx_params = (await self.prepare_transaction()) | {
                'value': 0,
            }
            
            transaction = await contract.functions.transfer(
                to_address,
                amount_to_transfer_in_wei,
            ).build_transaction(tx_params)
            
            return await self.send_transaction(transaction)
        except Exception as error:
            print(f'{error}')
            
