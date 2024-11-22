#  Задание от преподавателя

# Реализация собственного MEV-бота для арбитража через WebSocket
# Задание:
# В этом задании вы напишете код, который будет мониторить цены токенов USDT и DAI в пулах Uniswap по отношению к ETH, 
# используя WebSocket. Ваша задача — отслеживать изменения цен в реальном времени после каждой транзакции и 
# сравнивать их. Если обнаруживается спред (разница в цене), бот должен выводить информацию об этом в терминал.
# Шаги выполнения:
# 1. Инициализация и подключение через WebSocket:
# • Подключитесь к сети Ethereum через WebSocket.
# • Определите два пула: USDT/ETH и DAI/ETH, чтобы получать данные о транзакциях в этих пулах.
# 2. Парсинг цен USDT и DAI относительно ETH:
# • На старте программы получите текущие цены USDT и DAI относительно ETH из соответствующих пулов Uniswap.
# • Сохраните эти цены в переменные для последующего использования.
# 3. Мониторинг транзакций в пулах через WebSocket:
# • Используйте WebSocket для получения данных о событиях в пулах USDT/ETH и DAI/ETH.
# • Отслеживайте события типа Swap в этих пулах — после каждой транзакции получайте обновленную цену для USDT или DAI.
# 4. Сравнение цен после каждой транзакции:
# • После каждой транзакции обновляйте цену токена (USDT или DAI) в зависимости от того, 
# в каком пуле произошла транзакция.
# • Сравните обновленные цены USDT и DAI относительно ETH.
# 5. Проверка на спред:
# • Если спред между ценами USDT/ETH и DAI/ETH превышает заданный порог, выводите сообщение 
# об арбитражной возможности в терминал.
# • Пример сообщения: “Найден спред: цена USDT/ETH выше на 3% чем цена DAI/ETH.”
# Требования:
# 1. Подключение через WebSocket для мониторинга транзакций в пулах USDT/ETH и DAI/ETH.
# 2. Хранение и обновление цен USDT и DAI относительно ETH после каждой транзакции.
# 3. Сравнение цен и вывод в терминал информации о спреде, если он обнаружен.
# Пример выполнения:
# 1. Инициализация цен:
# Текущая цена USDT/ETH: 0.00067
# Текущая цена DAI/ETH: 0.00066

# # 2. Мониторинг и вывод:
# Новая транзакция в пуле USDT/ETH, цена обновлена: 0.00068
# Новая транзакция в пуле DAI/ETH, цена обновлена: 0.00064

# Найден спред: цена USDT/ETH выше на 2% чем цена DAI/ETH.


import asyncio

from client import Client
from settings import PRIVATE_KEY, PROXY, NETWORK_TO_WORK, ALCHEMY_WSS_URL

from modules.websockets.uniswap_mev_bot import UniswapMevBot


async def main() -> None:
    """
    Arbitrage MEV bot for Uniswap V3 pools ETH/USDT and ETH/DAI
    Connects via WebSocket to track price changes and identify arbitrage opportunities.

    Working only with Alchemy WebSocket provider
    https://docs.alchemy.com/docs/websocket-subscriptions
    """
    
    # Arbitrum ETH/USDT V3 pool
    # https://app.uniswap.org/explore/pools/arbitrum/0x641C00A822e8b671738d32a431a4Fb6074E5c79d
    ETH_USDT_UNISWAP_V3_POOL_ADDRESS = '0x641C00A822e8b671738d32a431a4Fb6074E5c79d' 
    # Arbitrum ETH/DAI V3 pool
    # https://app.uniswap.org/explore/pools/arbitrum/0xA961F0473dA4864C5eD28e00FcC53a3AAb056c1b
    ETH_DAI_UNISWAP_V3_POOL_ADDRESS = '0xA961F0473dA4864C5eD28e00FcC53a3AAb056c1b'
    SPREAD_PERCENTAGE_THRESHOLD = 0.2 # 0.2 = 0.2%, 1 = 1%, 2 = 2%

    
    client = Client(
        account_name="aiostudy", 
        network=NETWORK_TO_WORK,
        private_key=PRIVATE_KEY,
        proxy=PROXY,
    )
    
    async with client:
        uniswap_mev_bot = UniswapMevBot(
            client=client,
            wss_provider=ALCHEMY_WSS_URL,
            eth_usdt_pool_address=ETH_USDT_UNISWAP_V3_POOL_ADDRESS,
            eth_dai_pool_address=ETH_DAI_UNISWAP_V3_POOL_ADDRESS,
            spread_percentage_threshold=SPREAD_PERCENTAGE_THRESHOLD,
        )
        await uniswap_mev_bot.monitor_pools()


if __name__ == "__main__":
    asyncio.run(main())
