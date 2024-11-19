import asyncio
import time

from eth_abi import abi
from eth_account import Account

from zksync2.core.types import PaymasterParams
from zksync2.signer.eth_signer import PrivateKeyEthSigner
from zksync2.transaction.transaction_builders import TxFunctionCall
from zksync2.module.module_builder import ZkSyncBuilder
from zksync2.manage_contracts.paymaster_utils import PaymasterFlowEncoder

from custom_logger import logger
from client import Client
from config import (TOKENS_PER_CHAIN, CONTRACTS_PER_CHAIN, ZERO_ADDRESS, SYNCSWAP_ROUTER_V2_ABI, SYNCSWAP_POOL_ABI, 
                    SYNCSWAP_CLASSIC_FACTORY_ABI, ZKSYNC_SYNCSWAP_PAYMASTER_ABI)


class Syncswap:
    def __init__(self, client: Client) -> None:
        self.client: Client = client
        self.native_token = self.client.network.token
        self.router_address = CONTRACTS_PER_CHAIN[self.client.network.name]["SYNCSWAP_ROUTER_V2"]
        self.router_contract = self.client.get_contract(
            contract_address=self.router_address, abi=SYNCSWAP_ROUTER_V2_ABI
            )
        self.classic_factory_address = CONTRACTS_PER_CHAIN[self.client.network.name]["SYNCSWAP_CLASSIC_FACTORY"]
        self.classic_factory_contract = self.client.get_contract(
            contract_address=self.classic_factory_address, abi=SYNCSWAP_CLASSIC_FACTORY_ABI
        )

    async def get_pool_address(self, token_a: str, token_b: str) -> str:
        pool_address = await self.classic_factory_contract.functions.getPool(token_a, token_b).call()
        if pool_address != ZERO_ADDRESS:
            logger.debug(f"Found pool address for {token_a} and {token_b}: {pool_address}")
            return pool_address
        
        raise RuntimeError(f"Pool address is not found for {token_a} and {token_b}")
    
    async def calculate_min_liquidity(
        self, token_a: str, token_b: str, token_b_amount_wei: int, pool_address: str
        ) -> int:
        pool_contract = self.client.get_contract(
            contract_address=pool_address, abi=SYNCSWAP_POOL_ABI
        )
        
        total_liquidity_wei = await pool_contract.functions.totalSupply().call()
        total_liquidity_ether = self.client.from_wei(total_liquidity_wei)
        
        reserve_a_wei = await pool_contract.functions.reserve0().call()
        token_a_decimals = await self.client.get_decimals(token_address=await pool_contract.functions.token0().call())
        reserve_a_ether = self.client.from_wei(reserve_a_wei, token_a_decimals)
        
        reserve_b_wei = await pool_contract.functions.reserve1().call()
        reserve_b_ether = self.client.from_wei(reserve_b_wei)
        token_b_amount_ether = self.client.from_wei(token_b_amount_wei) / 2
        
        token_a_amount_ether = (reserve_a_ether * token_b_amount_ether) / reserve_b_ether
        
        min_liquidity_ether = ((total_liquidity_ether * token_a_amount_ether) / reserve_a_ether)
        min_liquidity_wei = self.client.to_wei(min_liquidity_ether)
        
        slippage = 2.142
        min_liquidity_wei_with_slippage = int(min_liquidity_wei * (1 - slippage / 100))
        logger.debug(f"Min liquidity with slippage: {min_liquidity_wei_with_slippage}")

        return min_liquidity_wei_with_slippage

    async def add_liquidity(
        self, token_a_name: str, token_a: str, token_b_name: str, token_b: str, amount_in: int
        ):
        
        pool_address = await self.get_pool_address(token_a, token_b)
        amount_in_wei = self.client.to_wei(amount_in)
        user_balance_wei = await self.client.w3.eth.get_balance(self.client.address)
        if user_balance_wei < amount_in_wei:
            raise RuntimeError(f"You dont have enough {self.client.network.token} on your balance! "
                               f"Your balance is {self.client.from_wei(user_balance_wei):.6f} "
                               f'"{self.client.network.token}". '
                               f"You want to add {amount_in} {token_a_name}")
        
        min_liquidity_wei = await self.calculate_min_liquidity(token_a, token_b, amount_in_wei, pool_address)
        
        logger.info(f"Start adding {amount_in} {token_a_name} liquidity to {token_a_name}/{token_b_name} "
                    f"pool on {self.client.network.name}")
        try:
            tx_params = (await self.client.prepare_transaction()) | {
                'value': amount_in_wei,
            }
            transaction = await self.router_contract.functions.addLiquidity2(
                pool_address,
                [
                    [
                        ZERO_ADDRESS,
                        amount_in_wei,
                        True
                    ],
                ],
                abi.encode(['address'], [self.client.address]),
                min_liquidity_wei,
                ZERO_ADDRESS,
                "0x",
                ZERO_ADDRESS,
            ).build_transaction(tx_params)
            return await self.client.send_transaction(transaction)
        except Exception as error:
            raise error
    
    async def remove_liquidity(self, token_a_name: str, token_a: str, token_b_name: str, token_b: str):
        pool_address = await self.get_pool_address(token_a, token_b)
        pool_contract = self.client.get_contract(
            contract_address=pool_address, abi=SYNCSWAP_POOL_ABI
        )
        
        liquidity_amount_wei = await pool_contract.functions.balanceOf(self.client.address).call()
        if liquidity_amount_wei == 0:
            raise RuntimeError(f"No liquidity to remove from {token_a_name}/{token_b_name} "
                               f"pool on {self.client.network.name}")
        
        reserve_ether_wei = await pool_contract.functions.reserve1().call()
        total_supply_wei = await pool_contract.functions.totalSupply().call()
        
        min_eth_amount_out = (liquidity_amount_wei * reserve_ether_wei / total_supply_wei) * 2
        slippage = 2.142
        min_eth_amount_out_with_slippage_wei = int(min_eth_amount_out * (1 - slippage / 100))
        min_eth_amount_out_with_slippage_ether = self.client.from_wei(min_eth_amount_out_with_slippage_wei)
        
        encoded_data = abi.encode(
            ['address', 'address', 'uint8'], 
            [token_a, self.client.address, 1],
            )
        
        logger.info(f"Start removing {min_eth_amount_out_with_slippage_ether:.6f} {token_a_name} "
                    f"liquidity from {token_a_name}/{token_b_name} pool on {self.client.network.name}")
        
        await self.client.check_for_approved(
            token_address=pool_address, 
            spender_address=self.router_address,
            amount_in_wei=liquidity_amount_wei,
            )

        await asyncio.sleep(15)
        
        try:
            tx_params = (await self.client.prepare_transaction()) | {
                'value': 0,
            }
            transaction = await self.router_contract.functions.burnLiquiditySingle(
                pool_address,
                liquidity_amount_wei,
                encoded_data,
                min_eth_amount_out_with_slippage_wei,
                ZERO_ADDRESS,
                "0x",
            ).build_transaction(tx_params)
            return await self.client.send_transaction(transaction)
        except Exception as error:
            raise error

    async def get_min_amount_out(self, pool_address: str, from_token_address: str, amount_in_wei: int, slippage: float):
        pool_contract = self.client.get_contract(
            contract_address=pool_address, abi=SYNCSWAP_POOL_ABI
        )
        min_amount_out = await pool_contract.functions.getAmountOut(
            from_token_address, amount_in_wei, self.client.address
        ).call()
        min_amount_out_with_slippage = int(min_amount_out * (1 - slippage / 100))
        return min_amount_out_with_slippage
    
    async def prepare_call_data_for_paymaster(
        self, 
        input_token_name: str, 
        output_token_name: str, 
        input_amount_ether: float, 
        slippage: float,
        ):
        
        input_token_address = TOKENS_PER_CHAIN[self.client.network.name][input_token_name]
        output_token_address = TOKENS_PER_CHAIN[self.client.network.name][output_token_name]
        input_token_decimals = await self.client.get_decimals(token_name=input_token_name)
        input_amount_wei = self.client.to_wei(input_amount_ether, input_token_decimals)
        logger.debug(f"Input token: {input_token_name}, output token: {output_token_name}")
        logger.debug(f"Input amount in wei: {input_amount_wei}")
        pool_address = await self.get_pool_address(input_token_address, output_token_address)
        logger.debug(f"Pool address: {pool_address}")
        
        min_amount_out_wei = await self.get_min_amount_out(pool_address, input_token_address, input_amount_wei, slippage)
        logger.debug(f"Min amount out: {min_amount_out_wei}")
        
        value = input_amount_wei if input_token_name == self.native_token else 0
        deadline = int(time.time() + 1200)
        withdraw_mode = 1  # unwrap wETH
        
        swap_data = abi.encode(
            ["address", "address", "uint8"],
            [input_token_address, self.client.address, withdraw_mode]
        )
        
        steps = [
            pool_address,
            swap_data,
            ZERO_ADDRESS,
            '0x',
            True
        ]
        
        paths = [
            [steps],
            input_token_address if not input_token_name == self.native_token else ZERO_ADDRESS,
            input_amount_wei,
        ]
        
        if input_token_name != self.native_token:
            await self.client.check_for_approved(
                token_address=input_token_address, spender_address=self.router_contract.address,
                amount_in_wei=input_amount_wei
            )
        
        tx_params = (await self.client.prepare_transaction()) | {
                'value': value,
            }
        transaction = await self.router_contract.functions.swap(
                [paths],
                min_amount_out_wei,
                deadline
            ).build_transaction(tx_params)
        
        return transaction

    async def swap(
        self, 
        input_token_name: str, 
        output_token_name: str, 
        input_amount_ether: float, 
        slippage: float, 
        token_name_for_paymaster_comission: str
        ):
        swap_transaction = await self.prepare_call_data_for_paymaster(
            input_token_name, output_token_name, input_amount_ether, slippage
        )

        # Create paymaster parameters
        paymaster_address = CONTRACTS_PER_CHAIN[self.client.network.name]["SYNCSWAP_PAYMASTER"]
        paymaster_contract = self.client.get_contract(
            contract_address=paymaster_address, abi=ZKSYNC_SYNCSWAP_PAYMASTER_ABI
        )
        token_address_for_paymaster_comission = (
            TOKENS_PER_CHAIN[self.client.network.name][token_name_for_paymaster_comission]
            )
        
        paymaster_input_data = paymaster_contract.encode_abi(
                abi_element_identifier='approvalBased',
                args=(
                    token_address_for_paymaster_comission,
                    2000000000,
                    "0x000000000000000000000000000000000000000000000000000000000000000f"
                )
            )

        paymaster_params = PaymasterParams(**{
            "paymaster": paymaster_address,
            "paymaster_input": self.client.w3.to_bytes(hexstr=paymaster_input_data)
        })

        tx_712 = TxFunctionCall(
            chain_id=int(swap_transaction['chainId']),
            nonce=int(swap_transaction['nonce']),
            from_=swap_transaction['from'],
            to=swap_transaction['to'],
            value=int(swap_transaction['value']) if input_token_name == self.native_token else 0,
            data=swap_transaction['data'],
            gas_price=int(swap_transaction['maxFeePerGas']),
            max_priority_fee_per_gas=int(swap_transaction['maxPriorityFeePerGas']),
            paymaster_params=paymaster_params
        ).tx712(int(swap_transaction['gas']))
        
        account = Account.from_key(self.client.private_key)
        signer = PrivateKeyEthSigner(account, self.client.chain_id)
        signed_message = signer.sign_typed_data(tx_712.to_eip712_struct())
        msg = tx_712.encode(signed_message)
        
        try:
            return await self.client.send_transaction(ready_tx=msg)
        except Exception as error:
            if 'Validation revert: Paymaster validation error: TF' in str(error):
                raise RuntimeError(f"Not enough {token_name_for_paymaster_comission} for paymaster comission")
            else:
                raise error
