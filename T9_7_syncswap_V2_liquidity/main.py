#  Задание от преподавателя

# Предоставление ликвидности на SyncSwap
# Задание:
# Напишите программу, которая предоставляет ликвидность в ETH на платформе SyncSwap для пула USDT-ETH, а затем выводит ее.
# Полезная информация:
# 1. Платформа SyncSwap
# 2. Адрес пула ликвидности 
# 3. Адреса контрактов в сети
# Шаги выполнения:
# 1. Настройка программы:
# • Пользователь должен указать в настройках:
# • Приватный ключ кошелька.
# • Количество ETH для предоставления в ликвидность.
# 2. Проверка настроек:
# • Программа проверяет, заполнены ли все обязательные настройки.
# • Если какая-то настройка не заполнена, выводится информативное сообщение об ошибке с указанием конкретной незаполненной настройки.
# 3. Проверка баланса:
# • Программа проверяет баланс кошелька пользователя.
# • Убедитесь, что средств достаточно для проведения транзакции с учетом суммы предоставления ликвидности и комиссии за газ.
# 4. Предоставление ликвидности:
# • Программа осуществляет предоставление ликвидности в пул USDT-ETH на платформе SyncSwap.
# • Используйте контракт роутера и вызывайте у него соответствующие функции для выполнения транзакции. 
# Также не забывайте про специальную математику расчета параметров транзакции.
# 5. Вывод ликвидности:
# • После предоставления ликвидности программа выполняет вывод ликвидности из пула.
# • Убедитесь, что транзакция вывода выполнена корректно и средства возвращены на кошелек пользователя.
# 6. Обработка транзакций:
# • Программа сохраняет хэши транзакций и ожидает их подтверждения.
# • После подтверждения выводится сообщение об успешном выполнении операций.
# Подсказки
# Подсказка №1:
# Для предоставления ликвидности, необходимо вызывать функцию addLiquidity
# Подсказка №2:
# Для вывода ликвидности, необходимо вызывать функцию burnLiquiditySingleWithPermit
# Подсказка №3:
# Используйте последний контракт роутера. Сами функции можно найти в первой версии контракта роутера

import asyncio

from client import Client
from settings import NETWORK_TO_WORK, PRIVATE_KEY, PROXY
from config import TOKENS_PER_CHAIN
from modules.dex.syncswap import Syncswap


async def main() -> None:
    """
    Syncswap V2 add/remove USDT-ETH liquidity (zkSync Era).
    """
    
    TOKEN_A: str = 'ETH'
    TOKEN_B: str = 'USDT'
    ETH_AMOUNT: float = 0.0001
    
    client = Client(
        account_name="aiostudy", 
        network=NETWORK_TO_WORK,
        private_key=PRIVATE_KEY,
        proxy=PROXY,
    )
    
    async with client:
        syncswap = Syncswap(client=client)
        await syncswap.add_liquidity(
            token_a_name=TOKEN_A,
            token_a=TOKENS_PER_CHAIN[NETWORK_TO_WORK.name][TOKEN_A],
            token_b_name=TOKEN_B,
            token_b=TOKENS_PER_CHAIN[NETWORK_TO_WORK.name][TOKEN_B],
            amount_in=ETH_AMOUNT,
        )
        
        await asyncio.sleep(10)
        
        await syncswap.remove_liquidity(
            token_a_name=TOKEN_A,
            token_a=TOKENS_PER_CHAIN[NETWORK_TO_WORK.name][TOKEN_A],
            token_b_name=TOKEN_B,
            token_b=TOKENS_PER_CHAIN[NETWORK_TO_WORK.name][TOKEN_B],
        )

if __name__ == "__main__":
    asyncio.run(main())
