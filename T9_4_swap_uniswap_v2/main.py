#  Задание от преподавателя

# Реализуйте свапы на сайте Uniswap в сети Arbitrum из ETH на любую другую монету. 
# Используйте документацию для V2 интерфейса свапов (swapExactETHForTokens).
# Предусмотрите следующие настройки:

#     Входящую и выходящую монету
#     Кол-во входящей монеты, которое мы хотим свапнуть
#     Slippage в %

# Сайт приложения
# Документация на V2 интерфейс
# Примечание 1. Сделайте возможность свапов из нативного токена и между ненативными токенами
# Примечание 2. Попробуйте добавить поддержку Optimism, BNB Chain и Polygon
# Подсказка 1. Контракт роутера в сети Arbitrum: 0x4752ba5dbc23f44d87826276bf6fd6b1c372ad24
# Подсказка 2. Для получения количества токенов на выходе, нужно дергать функцию getAmountsOut у контракта Quoter.
# Подсказка 3. path = [token_in_address, token_out_address]

import asyncio

from client import Client
from settings import NETWORK_TO_WORK, PRIVATE_KEY, PROXY
from config import TOKENS_PER_CHAIN
from modules.dex.uniswap_v2 import UniswapV2


async def main() -> None:
    """
    Uniswap V2 Swap
    """
    
    FROM_TOKEN: str = 'ETH' 
    TO_TOKEN: str = 'USDT'
    FROM_AMOUNT: float = 0.001 
    SLIPPAGE: float = 1 # 0.3 = 0.3%
    
    client = Client(
        account_name="aiostudy", 
        network=NETWORK_TO_WORK,
        private_key=PRIVATE_KEY,
        proxy=PROXY,
    )
    
    async with client:
        uniswap_v2 = UniswapV2(client=client)
        await uniswap_v2.swap(
            input_token=TOKENS_PER_CHAIN[NETWORK_TO_WORK.name][FROM_TOKEN], 
            input_token_name=FROM_TOKEN,
            output_token=TOKENS_PER_CHAIN[NETWORK_TO_WORK.name][TO_TOKEN], 
            output_token_name=TO_TOKEN,
            input_amount=FROM_AMOUNT, 
            slippage=SLIPPAGE
        )

if __name__ == "__main__":
    asyncio.run(main())
