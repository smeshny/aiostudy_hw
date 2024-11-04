# Реализовать работу агрегатора XY.finance через API интерфейс. 
# Для этой задачи вам необходимо сначала создать функцию отправки запросов, 
# которая позволит взаимодействовать с API. Следующим шагом сделайте получение всех необходимых 
# данных через методы Quote и Build tx. Когда получите данные с этих методов, 
# приступайте к созданию транзакции и ее отправкеПредусмотрите следующие настройки:

# Входящую и выходящую монетуКол-во входящей монеты, которое мы хотим свапнутьSlippage в %

# Сайт агрегатораДокументация Примечание 1. Сделайте простые свапы нативного токена и обратно для токенов USDT, USDC.

# Примечание 2. Добавьте возможность указывать свой собственный Slippage для свапов

# Примечание 3. Реализуйте поддержку BNB Chain, Arbitrum, Optimism, Polygon блокчейнов

# Подсказка 1. При свапах нативных монет, агрегаторы требуют использовать адреса-маски

# Подсказка 2. Не забывайте делать Approve перед свапами НЕ из нативных монет

# Подсказка 3. Value это не просто красивое слово

import asyncio

from client import Client
from settings import NETWORK_TO_WORK, PRIVATE_KEY, PROXY
from config import TOKENS_PER_CHAIN
from modules.dex.xy_finance import XYfinance


async def main() -> None:
    """
    XY.finance Swap
    """
    
    FROM_TOKEN: str = 'ETH' 
    TO_TOKEN: str = 'USDT'
    FROM_AMOUNT: float = 0.00001
    SLIPPAGE: float = 1 # 0.3 = 0.3%
    
    client = Client(
        account_name="aiostudy", 
        network=NETWORK_TO_WORK,
        private_key=PRIVATE_KEY,
        proxy=PROXY,
    )
    
    async with client:
        xy_finance = XYfinance(client=client)
        await xy_finance.swap(
            input_token=TOKENS_PER_CHAIN[NETWORK_TO_WORK.name][FROM_TOKEN], 
            input_token_name=FROM_TOKEN,
            output_token=TOKENS_PER_CHAIN[NETWORK_TO_WORK.name][TO_TOKEN], 
            output_token_name=TO_TOKEN,
            input_amount=FROM_AMOUNT, 
            slippage=SLIPPAGE
        )

if __name__ == "__main__":
    asyncio.run(main())
