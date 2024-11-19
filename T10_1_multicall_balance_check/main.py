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
from modules.dex.syncswap import Syncswap


async def main() -> None:
    """
    Multicall balance checker
    """
    
    NETWORK_TO_WORK: str = 'zkSync'
    TOKEN_FOR_PAYMASTER_COMISSION = 'USDC.e'
    FROM_TOKEN: str = 'USDT'
    TO_TOKEN: str = 'ETH'
    INPUT_AMOUNT: float = 6.018713
    SLIPPAGE: float = 1 # 0.3 = 0.3%

    
    client = Client(
        account_name="aiostudy", 
        network=get_network_by_name(NETWORK_TO_WORK),
        private_key=PRIVATE_KEY,
        proxy=PROXY,
    )
    
    async with client:
        syncswap = Syncswap(client=client)
        await syncswap.swap(
            input_token_name=FROM_TOKEN,
            output_token_name=TO_TOKEN,
            input_amount_ether=INPUT_AMOUNT,
            slippage=SLIPPAGE,
            token_name_for_paymaster_comission=TOKEN_FOR_PAYMASTER_COMISSION,
        )

if __name__ == "__main__":
    asyncio.run(main())
