import asyncio

from eth_abi import abi

from custom_logger import logger
from client import Client
from config import (CONTRACTS_PER_CHAIN, ZERO_ADDRESS, SYNCSWAP_ROUTER_V2_ABI, SYNCSWAP_POOL_ABI, 
                    SYNCSWAP_CLASSIC_FACTORY_ABI)


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
