#  Задание от преподавателя

# Бридж нативного токена в ERC20 токен другой сети на платформе Orbiter
# Задание:
# Напишите программу, которая осуществляет бридж нативного токена из одной сети в 
# ERC20 токен другой сети через платформу Orbiter.
# Полезная информация:
# 1. Платформа Orbiter
# 2. Краткое описание API Orbiter — тут
# 3. Примеры использования API для разных языков программирования — тут
# 4. Адреса контрактов поддерживаемых сетей — тут
# Шаги выполнения:
# 1. Настройка программы:
# • Пользователь должен указать в настройках:
# • Сеть-отправитель (из которой будет отправлен нативный токен).
# • Сеть-получатель (в которую будет получен ERC20 токен).
# • Приватный ключ кошелька.
# • Количество нативного токена для перевода.
# 2. Проверка настроек:
# • Программа проверяет, заполнены ли все обязательные настройки.
# • Если какая-то настройка не заполнена, выводится информативное сообщение об ошибке с указанием 
# конкретной незаполненной настройки.
# 3. Проверка баланса:
# • Программа проверяет баланс кошелька пользователя в сети-отправителе.
# • Убедитесь, что средств достаточно для проведения транзакции с учетом суммы перевода и комиссии за газ.
# 4. Выполнение бриджа:
# • Программа осуществляет бридж нативного токена через Orbiter.
# • Используйте соответствующие методы и API платформы Orbiter для выполнения транзакции.
# 5. Обработка транзакции:
# • Программа сохраняет хэш транзакции и ожидает ее подтверждения.
# • После подтверждения выводится сообщение об успешном выполнении операции.

import asyncio

from client import Client
from settings import NETWORK_TO_WORK, PRIVATE_KEY, PROXY
from config import TOKENS_PER_CHAIN
from modules.landings.zerolend import Zerolend


async def main() -> None:
    """
    Zerolend deposit/withdraw USDC on Linea network
    """
    
    TOKEN: str = 'USDC'
    AMOUNT: float = 1 # 0 if you want to deposit all your USDC
    
    client = Client(
        account_name="aiostudy", 
        network=NETWORK_TO_WORK,
        private_key=PRIVATE_KEY,
        proxy=PROXY,
    )
    
    async with client:
        zerolend = Zerolend(client=client)
        await zerolend.deposit_usdc(
            token_name=TOKEN,
            token_address=TOKENS_PER_CHAIN[NETWORK_TO_WORK.name][TOKEN],
            amount_to_deposit=AMOUNT,
        )
        
        await asyncio.sleep(15)
        
        await zerolend.withdraw_usdc(
            token_to_withdraw=TOKEN,
        )

if __name__ == "__main__":
    asyncio.run(main())
