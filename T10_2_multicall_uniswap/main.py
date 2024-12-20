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
from networks import get_network_by_name
from modules.dex.uniswap_v3 import UniswapV3, SwapPair


async def main() -> None:
    """
    Execute multiple token swaps on Uniswap V3 within a single transaction using Multicall.
    For TOKENS -> ETH direction doing one additional multicall approve transaction for spender.
    
    Optimizations:
    Multicall3 contract is used for fetching pools data from factory in one call.
    Also multicall3 is used for fetching erc20 tokens parameters for permit signature in one call.
    """
    
    NETWORK_TO_WORK: str = 'Arbitrum'
    
    SWAP_PAIRS: list[SwapPair] = [
        # ETH -> TOKENS
        SwapPair(from_token_name='ETH', to_token_name='USDT', from_amount=0.00005, slippage=1),
        SwapPair(from_token_name='ETH', to_token_name='DAI', from_amount=0.00005, slippage=1),
        SwapPair(from_token_name='ETH', to_token_name='USDC', from_amount=0.00005, slippage=1),
        SwapPair(from_token_name='ETH', to_token_name='USDC.e', from_amount=0.00005, slippage=1),
        SwapPair(from_token_name='ETH', to_token_name='WBTC', from_amount=0.00005, slippage=1),
        SwapPair(from_token_name='ETH', to_token_name='LINK', from_amount=0.00005, slippage=1),
        SwapPair(from_token_name='ETH', to_token_name='ARB', from_amount=0.00005, slippage=1),
        SwapPair(from_token_name='ETH', to_token_name='UNI', from_amount=0.00005, slippage=1),
        
        # TOKENS -> ETH
        # SwapPair(from_token_name='USDT', to_token_name='ETH', from_amount=0, slippage=1),
        # SwapPair(from_token_name='DAI', to_token_name='ETH', from_amount=0, slippage=1),
        # SwapPair(from_token_name='USDC', to_token_name='ETH', from_amount=0, slippage=1),
        # SwapPair(from_token_name='USDC.e', to_token_name='ETH', from_amount=0, slippage=1),
        # SwapPair(from_token_name='WBTC', to_token_name='ETH', from_amount=0, slippage=1),
        # SwapPair(from_token_name='LINK', to_token_name='ETH', from_amount=0, slippage=1),
        # SwapPair(from_token_name='ARB', to_token_name='ETH', from_amount=0, slippage=1),
        # SwapPair(from_token_name='UNI', to_token_name='ETH', from_amount=0, slippage=1),
        
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
        await uniswap_v3.multicall_swap(
            swap_pairs=SWAP_PAIRS
        )


if __name__ == "__main__":
    asyncio.run(main())
