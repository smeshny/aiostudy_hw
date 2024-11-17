#  Задание от преподавателя

# Stargate бридж (fast)
# Задание:
# Напишите программу, которая осуществляет мост (бридж) USDC/ETH через платформу Stargate в режиме fast.
# Полезная информация:
# 1. Платформа Stargate
# 2. Адреса контрактов поддерживаемых сетей — тут
# 3. Описание логики бриджа приведено тут
# Шаги выполнения:
# 1. Настройка программы:
# • Пользователь должен указать в настройках:
# • Сеть-отправитель (из которой будет отправлен токен).
# • Сеть-получатель (в которую будет получен токен).
# • Приватный ключ кошелька.
# • Количество USDC для перевода.
# 2. Проверка настроек:
# • Программа проверяет, заполнены ли все обязательные настройки.
# • Если какая-то настройка не заполнена, выводится информативное сообщение об ошибке с 
#   указанием конкретной незаполненной настройки.
# 3. Проверка баланса:
# • Программа проверяет баланс кошелька пользователя в сети-отправителе.
# • Убедитесь, что средств достаточно для проведения транзакции с учетом суммы перевода и комиссии за газ.
# 4. Выполнение бриджа:
# • В случае выбора пользователем токена USDC для бриджа, программа дает апррув (на сумма бриджа/весь 
#   баланс/максимальное значение) для необходимого контракта.
# • Программа осуществляет перевод токена через Stargate в режиме fast.
# • Используйте соответствующие контракты и их функции для выполнения транзакции.
# 5. Обработка транзакции:
# • Программа сохраняет хэш транзакции и ожидает ее подтверждения.
# • После подтверждения выводится сообщение об успешном выполнении операции.

import asyncio

from client import Client
from settings import PRIVATE_KEY, PROXY
from networks import get_network_by_name
from modules.bridges.orbiter import Orbiter


async def main() -> None:
    """
    Stargate V2 TAXI/BUS bridge (Arbitrum and Optimism chains only)
    !CAUTION!
    On stargate frontend they use Stargate V1 contracts, not V2.
    """
    
    SRC_TOKEN: str = 'ETH'
    SRC_CHAIN: str = 'Arbitrum'
    DST_TOKEN: str = 'ETH'
    DST_CHAIN: str = 'Optimism'
    AMOUNT: float = 0.002 
    BRIDGE_MODE: str = 'TAXI' # "TAXI" - fast and expensive, "BUS" - slow and cheap
    
    client = Client(
        account_name="aiostudy", 
        network=get_network_by_name(SRC_CHAIN),
        private_key=PRIVATE_KEY,
        proxy=PROXY,
    )
    
    async with client:
        orbiter = Orbiter(client=client)
        await orbiter.bridge(
            src_token_name=SRC_TOKEN,
            src_chain=get_network_by_name(SRC_CHAIN),
            dst_token_name=DST_TOKEN,
            dst_chain=get_network_by_name(DST_CHAIN),
            amount_to_bridge_ether=AMOUNT,
        )

if __name__ == "__main__":
    asyncio.run(main())
