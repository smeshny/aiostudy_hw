#  Задание от преподавателя

# Размещение USDC на ZeroLend
# Задание:
# Напишите программу, которая размещает USDC на лендинговой платформе ZeroLend.
# Полезная информация:
# 1. Платформа ZeroLend
# 2. Краткое описание процесса размещения токена на платформе тут
# 3. Контракты платформы тут
# Шаги выполнения:
# 1. Настройка программы:
# • Пользователь должен указать в настройках:
# • Приватный ключ кошелька.
# • Количество USDC для размещения.
# • Сеть, в которой будет происходить операция.
# 2. Проверка настроек:
# • Программа проверяет, заполнены ли все обязательные настройки.
# • Если какая-то настройка не заполнена, выводится информативное сообщение 
#  об ошибке с указанием конкретной незаполненной настройки.
# 3. Проверка баланса:
# • Программа проверяет баланс кошелька пользователя в USDC.
# • Убедитесь, что средств достаточно для проведения транзакции с учетом суммы размещения и комиссии за газ.
# 4. Выполнение размещения:
# • Программа дает апрув для токенов (сумма размещения/весь баланс/максимальный апрув) USDC соответствующему контракту.
# • Программа осуществляет размещение USDC на платформе ZeroLend.
# • Используйте соответствующие контракты ZeroLend для выполнения транзакции.
# 5. Обработка транзакции:
# • Программа сохраняет хэш транзакции и ожидает ее подтверждения.
# • После подтверждения выводится сообщение об успешном выполнении операции.

import asyncio

from client import Client
from settings import NETWORK_TO_WORK, PRIVATE_KEY, PROXY
from config import TOKENS_PER_CHAIN
from modules.landings.layerbank import Layerbank


async def main() -> None:
    """
    Zerolend deposit/withdraw USDC on Linea network
    """
    
    TOKEN: str = 'USDC'
    AMOUNT: float = 2 # 0 if you want to deposit all your USDC
    
    client = Client(
        account_name="aiostudy", 
        network=NETWORK_TO_WORK,
        private_key=PRIVATE_KEY,
        proxy=PROXY,
    )
    
    async with client:
        layerbank = Layerbank(client=client)
        await layerbank.deposit_usdc(
            token_name=TOKEN,
            token_address=TOKENS_PER_CHAIN[NETWORK_TO_WORK.name][TOKEN],
            amount_to_deposit=AMOUNT,
        )
        
        await asyncio.sleep(15)
        
        await layerbank.withdraw_usdc(
            token_to_withdraw=TOKEN,
        )

if __name__ == "__main__":
    asyncio.run(main())
