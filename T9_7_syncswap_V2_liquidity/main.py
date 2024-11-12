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
from modules.dex.izumi import Izumi


async def main() -> None:
    """
    Izumi V3 swaps (Scroll, Linea).
    Another networks have problems with liquidity.
    You can try Arbitrum, but it's not recommended. Be careful with USDC and USDC.e
    Please, set preferred network in settings.py.
    
    !Caution!
    
    Double check the token addresses on Izumi frontend before swapping!
    Protection enabled! If ODOS quote is better than Izumi V3 quote by more than 5%, the swap will be cancelled.
    Set FROM_AMOUNT = 0 if you want to swap all balance of ERC20 token
    Please, remember that you can't swap all balance of native token!
    You can't swap ETH->WETH or WETH->ETH, because it's not a swap, it's wrap or unwrap
    """
    
    FROM_TOKEN: str = 'ETH'
    TO_TOKEN: str = 'USDT'
    FROM_AMOUNT: float = 0.001 # Choose 0 if you want to swap all balance of ERC20 token
    SLIPPAGE: float = 1 # 0.3 = 0.3%
    
    client = Client(
        account_name="aiostudy", 
        network=NETWORK_TO_WORK,
        private_key=PRIVATE_KEY,
        proxy=PROXY,
    )
    
    async with client:
        izumi = Izumi(client=client)
        await izumi.swap(
            input_token=TOKENS_PER_CHAIN[NETWORK_TO_WORK.name][FROM_TOKEN], 
            input_token_name=FROM_TOKEN,
            output_token=TOKENS_PER_CHAIN[NETWORK_TO_WORK.name][TO_TOKEN], 
            output_token_name=TO_TOKEN,
            input_amount=FROM_AMOUNT, 
            slippage=SLIPPAGE
        )

if __name__ == "__main__":
    asyncio.run(main())
