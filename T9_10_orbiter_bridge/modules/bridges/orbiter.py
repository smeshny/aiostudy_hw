import asyncio

from custom_logger import logger
from client import Client
from config import TOKENS_PER_CHAIN


class Orbiter:
    def __init__(self, client: Client) -> None:
        self.client: Client = client
        self.native_token = self.client.network.token
        
        self.layerbank_core_address = CONTRACTS_PER_CHAIN[self.client.network.name]["LAYERBANK_CORE"]
        self.layerbank_core_contract = self.client.get_contract(
            contract_address=self.layerbank_core_address, abi=LAYERBANK_CORE_ABI
            )

    async def deposit_usdc(self, token_name: str, token_address: str, amount_to_deposit: float):
        token_decimals = await self.client.get_decimals(token_address=token_address)
        amount_to_deposit_wei = self.client.to_wei(amount_to_deposit, token_decimals)
        usdc_balance_wei = await self.client.get_erc20_balance(token_address=token_address)
        
        if amount_to_deposit == 0:
            amount_to_deposit_wei = usdc_balance_wei
        
        if usdc_balance_wei < amount_to_deposit_wei:
            raise RuntimeError(f"You don't have enough {token_name} to deposit to "
                               f"Layerbank in {self.client.network.name}. "
                               f"Your balance is "
                               f"{self.client.from_wei(usdc_balance_wei, token_decimals):.2f} {token_name}")
        
        logger.info(f"Starting deposit {self.client.from_wei(amount_to_deposit_wei, token_decimals):.2f} "
                    f"{token_name} to Layerbank in {self.client.network.name}")
        
        await self.client.check_for_approved(
            token_address=token_address,
            spender_address=self.layerbank_core_address,
            amount_in_wei=amount_to_deposit_wei,
        )
        
        try:
            tx_params = (await self.client.prepare_transaction()) | {
                'value': 0,
            }
            transaction = await self.layerbank_core_contract.functions.supply(
                CONTRACTS_PER_CHAIN[self.client.network.name]["LAYERBANK_IUSDC_CONTRACT"],
                amount_to_deposit_wei,
            ).build_transaction(tx_params)
            return await self.client.send_transaction(transaction)
        except Exception as error:
            raise error

    async def withdraw_usdc(self, token_to_withdraw: str):
        iusdc_address = CONTRACTS_PER_CHAIN[self.client.network.name]["LAYERBANK_IUSDC_CONTRACT"]
        iusdc_balance_wei = await self.client.get_erc20_balance(token_address=iusdc_address)
        
        if iusdc_balance_wei == 0:
            raise RuntimeError("You don't have USDC to withdraw")
        
        logger.info(f"Starting withdraw all {token_to_withdraw} from Layerbank in {self.client.network.name}")
        
        await self.client.check_for_approved(
            token_address=iusdc_address,
            spender_address=self.layerbank_core_address,
            amount_in_wei=iusdc_balance_wei,
        )
        
        try:
            tx_params = (await self.client.prepare_transaction()) | {
                'value': 0,
            }
            transaction = await self.layerbank_core_contract.functions.redeemToken(
                iusdc_address,
                iusdc_balance_wei,
            ).build_transaction(tx_params)
            return await self.client.send_transaction(transaction)
        except Exception as error:
            raise error
