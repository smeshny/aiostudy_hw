#  Задание от преподавателя

# Использование SDK zksync2
# Задание:
# Напишите программу, которая осуществляет свап любого токена на другой с помощью используя SDK zksync2.
# Полезная информация:
# 1. Платформа SyncSwap
# 2. SDK zksync2
# 4. Документация по SDK zksync2 тут.
# 5. Примеры использования SDK zksync2 тут.
# Шаги выполнения:
# 1. Настройка программы:
# • Пользователь должен указать в настройках:
# • Приватный ключ кошелька.
# • Входящий токен.
# • Выходящий токен.
# • Количество входящего токена для свапа.
# 2. Проверка настроек:
# • Программа проверяет, заполнены ли все обязательные настройки.
# • Если какая-то настройка не заполнена, выводится информативное сообщение об ошибке с указанием 
#   конкретной незаполненной настройки.
# 3. Проверка баланса:
# • Программа проверяет баланс кошелька пользователя во входящем токене.
# • Убедитесь, что средств достаточно для проведения транзакции с учетом суммы свапа и комиссии за газ.
# 4. Выполнение свапа:
# • Программа осуществляет свап выбранного токена на другой используя SDK zksync2.
# • Используйте соответствующие методы и API SDK zksync2 для выполнения транзакции.
# 5. Обработка транзакции:
# • Программа сохраняет хэш транзакции и ожидает ее подтверждения.
# • После подтверждения выводится сообщение об успешном выполнении операции.

import asyncio

from client import Client
from settings import PRIVATE_KEY, PROXY
from networks import get_network_by_name
from modules.dex.syncswap import Syncswap


async def main() -> None:
    """
    Syncswap swap with paymaster and zksync2 python sdk
    """
    
    NETWORK_TO_WORK: str = 'zkSync'
    TOKEN_FOR_PAYMASTER_COMISSION = 'USDC.e'
    FROM_TOKEN: str = 'USDT'
    TO_TOKEN: str = 'ETH'
    INPUT_AMOUNT: float = 111
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
