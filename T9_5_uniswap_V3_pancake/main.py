# Реализуйте свапы на PancakeSwap с использованием UniswapV3 интерфейса в сети Arbitrum. 
# Финальная транзакция будет использования метода multicall, 
# что значит использование сразу нескольких запросов к контракту.

# Предусмотрите следующие настройки:

# Входящую и выходящую монетуКол-во входящей монеты, которое мы хотим свапнутьSlippage в %

# Сайт приложенияДокументация UniswapV3

# Примечание 1. Добавьте возможность свапа как конкретного количества монет, так и всего баланса.

# Примечание 2. Добавьте поддержку Optimism, BNB Chain, Polygon.

# Примечание 3. Используйте только ликвидные пулы при свапах 
# (токены не должны быть без ликвидность, иначе у них будет слипадж >10%). 

# Подсказка 1. V3 интерфейс свапов - это методы quoteExactInput и exactInput

# Подсказка 2. Не забудьте делать refund или unwrap после свапа

import asyncio

from client import Client
from settings import NETWORK_TO_WORK, PRIVATE_KEY, PROXY
from config import TOKENS_PER_CHAIN
from modules.dex.pancakeswap import Pancakeswap


async def main() -> None:
    """
    Pancakeswap V3 (BNB Chain and Arbitrum)
    Set FROM_AMOUNT = 0 if you want to swap all balance of ERC20 token
    Please, remember that you can't swap all balance of native token!
    You can't swap ETH->WETH or WETH->ETH, because it's not a swap, it's wrap or unwrap
    """
    
    FROM_TOKEN: str = 'USDT'
    TO_TOKEN: str = 'ETH'
    FROM_AMOUNT: float = 0 # Choose 0 if you want to swap all balance of ERC20 token
    SLIPPAGE: float = 1 # 0.3 = 0.3%
    
    client = Client(
        account_name="aiostudy", 
        network=NETWORK_TO_WORK,
        private_key=PRIVATE_KEY,
        proxy=PROXY,
    )
    
    async with client:
        pancakeswap = Pancakeswap(client=client)
        await pancakeswap.swap(
            input_token=TOKENS_PER_CHAIN[NETWORK_TO_WORK.name][FROM_TOKEN], 
            input_token_name=FROM_TOKEN,
            output_token=TOKENS_PER_CHAIN[NETWORK_TO_WORK.name][TO_TOKEN], 
            output_token_name=TO_TOKEN,
            input_amount=FROM_AMOUNT, 
            slippage=SLIPPAGE
        )

if __name__ == "__main__":
    asyncio.run(main())
