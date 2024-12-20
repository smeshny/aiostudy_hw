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

from modules.websockets.uniswap_monitor import UniswapMonitor


async def main() -> None:
    """
    Uniswap WebSocket monitor for pool events
    You can choose any events to listen in UniswapV3Pool contract
    Most popular events: Swap, Burn, Mint, Flash, Collect, Initialize, CollectProtocol
    """
    
    
    UNISWAP_V3_POOL_ADDRESS = '0xC6962004f452bE9203591991D15f6b388e09E8D0' # Arbitrum ETH/USDC V3 pool
    # Events to listen:
    EVENTS_TO_LISTEN = ['Swap', 'Burn', 'Mint', 'Collect', 'Initialize', 'CollectProtocol'] 

    
    client = Client(
        account_name="aiostudy", 
        network=NETWORK_TO_WORK,
        private_key=PRIVATE_KEY,
        proxy=PROXY,
    )
    
    async with client:
        uniswap_monitor = UniswapMonitor(
            client=client,
            wss_provider=ALCHEMY_WSS_URL,
            pool_address=UNISWAP_V3_POOL_ADDRESS,
            events_to_listen=EVENTS_TO_LISTEN,
            )
        await uniswap_monitor.monitor_pool()


if __name__ == "__main__":
    asyncio.run(main())
