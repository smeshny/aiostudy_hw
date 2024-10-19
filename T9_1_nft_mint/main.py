# Задание: Подписание и проверка типизированных сообщений

# Подпишите типизированное сообщение на сайте Uniswap и получите с него сигнатуру. 
# После этого проверьте, действительно ли данная сигнатура валидна для исходного сообщения. 

# Подсказка 1. Подпись инициализируется при свапах из НЕнативных токенов

import asyncio

from client import Client
from modules.uniswap import Uniswap
from settings import NETWORK_TO_WORK, PRIVATE_KEY, PROXY
from config import TOKENS_PER_CHAIN, CONTRACTS_PER_CHAIN


async def main() -> None:
    """
    Sign an ERC20 swap permit for Uniswap and get the signature.
    """
    
    TOKEN_TO_SPEND = TOKENS_PER_CHAIN[NETWORK_TO_WORK.name]['USDC.e']
    ROUTER_ADDRESS = CONTRACTS_PER_CHAIN[NETWORK_TO_WORK.name]['UNISWAP_UNIVERSAL_ROUTER_4']
    VALUE_TO_SEND = 10
    
    
    client = Client(
        account_name="aiostudy", 
        network=NETWORK_TO_WORK,
        private_key=PRIVATE_KEY,
        proxy=PROXY,
    )
    async with client:
        uniswap = Uniswap(client=client)
        
        signed_message = await uniswap.sign_erc20_swap_permit(
            erc20_address_to_spend=TOKEN_TO_SPEND,
            spender_contract_address=ROUTER_ADDRESS,
            amount_ether=VALUE_TO_SEND,
        )
        print(signed_message)

if __name__ == "__main__":
    asyncio.run(main())
