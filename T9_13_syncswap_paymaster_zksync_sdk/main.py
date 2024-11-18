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
# • Если какая-то настройка не заполнена, выводится информативное сообщение об ошибке с указанием конкретной незаполненной настройки.
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
from modules.claim_simulation import ClaimSimulation


async def main() -> None:
    """
    Calim simulation on DropManager contract
    This script will claim all available tokens from DropManager contract.
    You can specify amount of tokens to claim per each transaction.
    """
    
    AMOUNT_TO_CLAIM_PER_TRANSACTION: float = 4.20 # amount of tokens to claim per each transaction
    NETWORK_TO_WORK: str = 'Arbitrum'
    
    client = Client(
        account_name="aiostudy", 
        network=get_network_by_name(NETWORK_TO_WORK),
        private_key=PRIVATE_KEY,
        proxy=PROXY,
    )
    
    async with client:
        claim_simulation = ClaimSimulation(client=client)
        await claim_simulation.claim_all_tokens(amount_to_claim_per_transaction_ether=AMOUNT_TO_CLAIM_PER_TRANSACTION)

if __name__ == "__main__":
    asyncio.run(main())
