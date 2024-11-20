#  Задание от преподавателя

# Сделать несколько свапов за раз на Uniswap, используя Multicall
# Задание:
# Необходимо реализовать выполнение нескольких обменов (свапов) токенов на Uniswap в рамках одной транзакции с 
# использованием механизма Multicall. Это позволяет объединить несколько операций в одну, 
# что сокращает затраты на газ и увеличивает эффективность транзакций.
# Шаги выполнения:
# 1. Подготовка данных для свапов:
# • Определите токены и количество для каждого свапа.
# • Подготовьте маршруты свапов для каждого из токенов (например, обмен ETH на USDT и ETH на DAI).
# 2. Создание транзакции Multicall:
# • Используйте контракт Multicall для объединения нескольких вызовов 
# swapExactTokensForTokens или swapExactETHForTokens.
# • Сформируйте список операций для выполнения в рамках одной транзакции.
# 3. Подпись и отправка транзакции:
# • Подпишите и отправьте транзакцию с несколькими свапами на Uniswap.
# 4. Подтверждение выполнения:
# • Дождитесь подтверждения выполнения транзакции и проверьте результаты всех свапов.
# Требования:
# 1. Подготовить несколько операций свапов на Uniswap.
# 2. Объединить их в одну транзакцию с использованием Multicall.
# 3. Подписать и отправить транзакцию, дождаться подтверждения.

import asyncio

from client import Client
from settings import PRIVATE_KEY, PROXY
from config import TOKENS_PER_CHAIN
from networks import get_network_by_name
from modules.dex.uniswap_v3 import UniswapV3, SwapPair


async def main() -> None:
    """
    Uniswap v3 multicall swap for 2 pairs e.g. ETH->USDT and ETH->DAI
    Multicall swap perform in single transaction
    """
    
    NETWORK_TO_WORK: str = 'Arbitrum'
    
    SWAP_PAIRS: list[SwapPair] = [
        # SwapPair(from_token_name='ETH', to_token_name='USDT', from_amount=0.0001, slippage=1),
        # SwapPair(from_token_name='ETH', to_token_name='DAI', from_amount=0.0001, slippage=1),
        SwapPair(from_token_name='USDT', to_token_name='ETH', from_amount=0, slippage=1),
        SwapPair(from_token_name='DAI', to_token_name='ETH', from_amount=0, slippage=1),
        
        # Add more SwapPair instances as needed
    ]

    client = Client(
        account_name="aiostudy", 
        network=get_network_by_name(NETWORK_TO_WORK),
        private_key=PRIVATE_KEY,
        proxy=PROXY,
    )
    
    async with client:
        uniswap_v3 = UniswapV3(client=client)
        await uniswap_v3.multicallswap(
            swap_pairs=SWAP_PAIRS
        )


if __name__ == "__main__":
    asyncio.run(main())
