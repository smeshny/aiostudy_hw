# Задание: L2pass минтер

# Настало время применить все наши навыки, ради нашей главной цели - минта джипега.

# Сделайте минт NFT на сайте https://l2pass.com/mint в сети Arbitrum. 
# Контракт простенький, но учитывайте изменении цены владельцем коллекции - получайте эту цену динамично

# Предусмотрите следующие настройки:

# Сеть минта NFTКоличество NFT к минту

# Примечание 1. Не ограничивайтесь только одной сетью, попробуйте реализовать сразу несколько поддерживаемых сетей

# Примечание 2. Предусмотрите возможность минтить сразу несколько NFT в одной транзации  
# Подсказка 1. Коммисию за минт можно получить с помощью разных функций, 
# но обычно это что-то из разряда: mintFee, Fee, mintPrice, Price

import asyncio

from client import Client
from modules.l2_pass import L2Pass
from settings import NETWORK_TO_WORK, PRIVATE_KEY, PROXY
from config import TOKENS_PER_CHAIN, CONTRACTS_PER_CHAIN


async def main() -> None:
    """
    Mint L2PASS nft.
    """
    
    L2_PASS_NFT_QUANTITY: int = 2
    
    client = Client(
        account_name="aiostudy", 
        network=NETWORK_TO_WORK,
        private_key=PRIVATE_KEY,
        proxy=PROXY,
    )
    
    async with client:
        l2_pass = L2Pass(client=client)
        await l2_pass.mint(nft_quantity=L2_PASS_NFT_QUANTITY)

if __name__ == "__main__":
    asyncio.run(main())
