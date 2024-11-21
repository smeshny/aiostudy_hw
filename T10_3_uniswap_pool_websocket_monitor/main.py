#  Задание от преподавателя

# Мониторинг пула на Uniswap и получение событий через WebSocket
# Описание задания:
# Напишите код, который будет отслеживать события определенного пула на Uniswap (например, Swap, Mint, Burn)
# в реальном времени с использованием WebSocket.
# Шаги выполнения:
# 1. Подключитесь к сети Ethereum через WebSocket.
# 2. Определите адрес пула Uniswap, который необходимо мониторить (например, USDC/ETH или DAI/ETH).
# 3. Используя ABI пула, получайте события типа Swap, Mint, и Burn.
# 4. Обрабатывайте события, выводя на экран важные данные 
# (например, адреса участников, объемы обменов или ликвидности).
# Требования:
# 1. Подключение через WebSocket.
# 2. Мониторинг пула и получение событий в реальном времени.
# 3. Обработка и вывод данных по событиям.

import asyncio

from client import Client
from settings import PRIVATE_KEY, PROXY, NETWORK_TO_WORK, ALCHEMY_WSS_URL

from modules.dex.uniswap_v3 import UniswapV3, SwapPair


async def main() -> None:
    """
    Uniswap WebSocket monitor for pool events
    """

    client = Client(
        account_name="aiostudy", 
        network=NETWORK_TO_WORK,
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
