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
from networks import get_network_by_name
from modules.bridges.orbiter import Orbiter


async def main() -> None:
    """
    Orbiter bridge
    """
    
    SRC_TOKEN: str = 'ETH'
    SRC_CHAIN: str = 'Arbitrum'
    DST_TOKEN: str = 'ETH'
    DST_CHAIN: str = 'Optimism'
    AMOUNT: float = 0.002 
    
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
            src_token_address=TOKENS_PER_CHAIN[NETWORK_TO_WORK.name][SRC_TOKEN],
            src_chain=get_network_by_name(SRC_CHAIN),
            dst_token_name=DST_TOKEN,
            dst_token_address=TOKENS_PER_CHAIN[NETWORK_TO_WORK.name][DST_TOKEN],
            dst_chain=get_network_by_name(DST_CHAIN),
            amount_to_bridge_ether=AMOUNT,
        )

if __name__ == "__main__":
    asyncio.run(main())
