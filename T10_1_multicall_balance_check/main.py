#  Задание от преподавателя

# Проверка балансов нескольких кошельков с помощью Multicall
# Задание:
# Напишите программу, которая проверяет балансы нескольких кошельков одновременно, используя технологию Multicall.
# Полезная информация:
# 1. Технология Multicall позволяет объединять несколько вызовов смарт-контрактов 
# в один, что снижает количество запросов и повышает эффективность.
# 2. Адреса контрактов Multicall для разных сетей можно найти в приложенном файле.
# 3. Примеры использования Multicall можно через эксплореры по конкретным контрактам.
# Шаги выполнения:
# 1. Настройка программы:
# • Пользователь должен указать в настройках:
# • Список адресов кошельков, балансы которых необходимо проверить.
# • Сеть, в которой будут проверяться балансы.
# 2. Проверка настроек:
# • Программа проверяет, заполнены ли все обязательные настройки.
# • Если какая-либо настройка не заполнена, выводится информативное сообщение об ошибке с указанием 
# конкретной незаполненной настройки.
# 3. Получение балансов с помощью Multicall:
# • Программа формирует вызовы для получения балансов указанных кошельков.
# • Использует контракт Multicall для выполнения всех запросов за один вызов.
# • При необходимости учитывает балансы как нативных токенов, так и ERC20 токенов.
# 4. Обработка результатов:
# • Программа обрабатывает результаты вызова Multicall и получает балансы каждого кошелька.
# • Выводит пользователю список адресов с соответствующими балансами в удобном формате.
# 5. Обработка ошибок:
# • Программа должна корректно обрабатывать возможные ошибки при вызове Multicall.
# • В случае ошибки выводится соответствующее сообщение пользователю.

import asyncio

from client import Client
from settings import PRIVATE_KEY, PROXY
from networks import get_network_by_name
from modules.multicall_functions import Multicall3


async def main() -> None:
    """
    Multicall balance checker
    """
    
    NETWORK_TO_WORK: str = 'Arbitrum'
    TOKENS_TO_CHECK: list[str] = [
        'WETH',
        'USDC.e', 
        'USDT',
        'ARB',
        'DAI',
        'OX',
        'ADP'
    ]
    WALLETS_TO_CHECK: list[str] = [
        '0x0D0707963952f2fBA59dD06f2b425ace40b492Fe', # Arbitrum Gate.io hot wallet
        '0x5bdf85216ec1e38D6458C870992A69e38e03F7Ef', # Arbitrum Bitget 2 hot wallet
        '0xDBF5E9c5206d0dB70a90108bf936DA60221dC080', # Arbitrum Wintermute hot wallet
        '0xf92402bB795Fd7CD08fb83839689DB79099C8c9C', # Binance 6
        '0x1B5B4e441F5A22bfd91B7772C780463F66A74b35', # Binance 56
        '0xB38e8c17e38363aF6EbdCb3dAE12e0243582891D', # Binance 54
        '0x490b1E689Ca23be864e55B46bf038e007b528208', # Kraken 2
        '0xbFc1FECa8B09A5c5D3EFfE7429eBE24b9c09EF58', # Arbitrum Foundation: L2 Treasury Timelock
        '0x82CbeCF39bEe528B5476FE6d1550af59a9dB6Fc0', # Stargate Finance
        '0x0938C63109801Ee4243a487aB84DFfA2Bba4589e', # OKX
        '0xe93685f3bBA03016F02bD1828BaDD6195988D950', # Layer Zero: Executor
    ]

    client = Client(
        account_name="aiostudy", 
        network=get_network_by_name(NETWORK_TO_WORK),
        private_key=PRIVATE_KEY,
        proxy=PROXY,
    )
    
    async with client:
        multicall = Multicall3(client=client)
        await multicall.get_balances(
            tokens_to_check=TOKENS_TO_CHECK,
            wallets_to_check=WALLETS_TO_CHECK
            )


if __name__ == "__main__":
    asyncio.run(main())
