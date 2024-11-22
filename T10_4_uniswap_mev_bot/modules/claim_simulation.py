import asyncio

from custom_logger import logger
from client import Client
from config import CONTRACTS_PER_CHAIN, DROP_MANAGER_SIMULATION_ABI


class ClaimSimulation:
    def __init__(self, client: Client) -> None:
        self.client: Client = client
        self.native_token = self.client.network.token
        self.drop_manager_address = CONTRACTS_PER_CHAIN[self.client.network.name]["DROP_MANAGER_SIMULATION"]
        self.drop_manager_contract = self.client.get_contract(
            contract_address=self.drop_manager_address, abi=DROP_MANAGER_SIMULATION_ABI
            )

    async def register(self) -> None:
        is_registered = await self.drop_manager_contract.functions.registeredUsers(self.client.address).call()
        if not is_registered:
            logger.info(f"{self.client.address} not registered. Start registration process...")
            try:
                tx_params = (await self.client.prepare_transaction()) | {
                    'value': 0,
                }
                transaction = await self.drop_manager_contract.functions.register().build_transaction(tx_params)
                await self.client.send_transaction(transaction)
                logger.success(f"{self.client.address} successfully registered")
                logger.info(f"Waiting for 5 seconds before next step...")
                await asyncio.sleep(5)
            except Exception as error:
                raise RuntimeError(f"Error during registration: {error}")
        else:
            logger.success(f"{self.client.address} already registered")
    
    async def get_claimable_amount(self) -> None:
        claimable_amount_wei = await self.drop_manager_contract.functions.claimableTokens(self.client.address).call()
        claimable_amount_ether = self.client.from_wei(claimable_amount_wei)
        logger.info(f"Claimable amount: {claimable_amount_ether}")
        return claimable_amount_wei
    
    async def claim_exact_amount(
        self, amount_to_claim_per_transaction_ether: float, amount_to_claim_per_transaction_wei: int
        ) -> None:
            logger.info(f"Start claim {amount_to_claim_per_transaction_ether} ADP tokens")
            try:
                tx_params = (await self.client.prepare_transaction()) | {
                    'value': 0,
                }
                transaction = await self.drop_manager_contract.functions.claim(
                    amount_to_claim_per_transaction_wei
                    ).build_transaction(tx_params)
                await self.client.send_transaction(transaction)
                
                logger.info(f"Successfully claimed {amount_to_claim_per_transaction_ether} tokens")
                logger.info(f"Waiting for 10 seconds before next transaction")
                await asyncio.sleep(10)
            except Exception as error:
                raise RuntimeError(f"Error during claiming: {error}")
            
    async def claim_all_tokens(self, amount_to_claim_per_transaction_ether: float) -> None:
        await self.register()
        amount_to_claim_per_transaction_wei = self.client.to_wei(amount_to_claim_per_transaction_ether)

        while True:
            claimable_amount = await self.get_claimable_amount()
            
            if claimable_amount == 0:
                logger.success(f"You have claimed all available tokens. No more tokens to claim")
                break
            
            if claimable_amount < amount_to_claim_per_transaction_wei:
                logger.warning(f"Claimable amount is less than {amount_to_claim_per_transaction_ether} ADP tokens")
                logger.warning(f"It will be the last claim.")
                
                amount_to_claim_per_transaction_wei = claimable_amount
                amount_to_claim_per_transaction_ether = self.client.from_wei(amount_to_claim_per_transaction_wei)
                await self.claim_exact_amount(
                    amount_to_claim_per_transaction_ether, amount_to_claim_per_transaction_wei
                    )
                break

            await self.claim_exact_amount(amount_to_claim_per_transaction_ether, amount_to_claim_per_transaction_wei)
        
        total_balance_adp_wei = await self.client.get_erc20_balance('ADP')
        total_balance_adp_ether = self.client.from_wei(total_balance_adp_wei)
        
        logger.success(f"Final balance of ADP tokens: {total_balance_adp_ether}")
