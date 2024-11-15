#  Задание от преподавателя

# Размещение USDC на LayerBank
# Задание:
# Напишите программу, которая размещает USDC в сети Scroll на лендинговой платформе LayerBank.
# Полезная информация:
# 1. Платформа LayerBank
# 2. Контракты платформы тут
# 3. Описание лендинговой логики тут
# Шаги выполнения:
# 1. Настройка программы:
# Пользователь должен указать в настройках:
# • Приватный ключ кошелька.
# • Количество USDC для размещения.
# • Сеть (Scroll).
# 2. Проверка настроек:
# • Программа проверяет, заполнены ли все обязательные настройки.
# • Если какая-то настройка не заполнена, выводится информативное сообщение об ошибке с указанием конкретной незаполненной настройки.
# 3. Проверка баланса:
# • Программа проверяет баланс кошелька пользователя в USDC.
# • Убедитесь, что средств достаточно для проведения транзакции с учетом суммы размещения и комиссии за газ.
# 4. Выполнение размещения:
# • Программа осуществляет размещение USDC на платформе LayerBank в сети Scroll.
# • Используйте контракты и соответствующие их методы платформы LayerBank в сети Scroll для выполнения транзакции.
# 5. Обработка транзакции:
# • Программа сохраняет хэш транзакции и ожидает ее подтверждения.
# • После подтверждения выводится сообщение об успешном выполнении операции.

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
