#  Задание от преподавателя

# Симуляция клейма дропа
# Задание:
# Напишите программу, которая симулирует процесс клейма (claim) токенов из дропа по указанному контракту.
# Полезная информация:
# 1. Адрес контракта: 0x060e7c1bc320C9e7C1760e06A5455c343D16603B
# 2. Функции контракта:
# • register: регистрирует адрес пользователя, добавляя его в маппинг и предоставляя возможность получить 25 токенов.
# • claim: позволяет клеймить определенное количество токенов. Клеймить можно несколько раз, 
# пока есть доступные токены (например, 5 раз по 5 токенов). После получения всех 25 токенов 
# дальнейшие вызовы невозможны.
# • getClaimableAmount: возвращает количество токенов, доступных для клейма на данный момент.
# Шаги выполнения:
# 1. Настройка программы:
# • Пользователь должен указать в настройках:
# • Приватный ключ кошелька.
# • Количество токенов для клейма при каждом вызове функции claim.
# 2. Проверка настроек:
# • Программа проверяет, заполнены ли все обязательные настройки.
# • Если какая-либо настройка не заполнена, выводится информативное сообщение об ошибке с указанием 
# конкретной незаполненной настройки.
# 3. Регистрация пользователя:
# • Программа вызывает функцию register контракта, чтобы зарегистрировать адрес пользователя и получить возможность 
# клеймить токены.
# 4. Проверка доступных токенов:
# • Программа вызывает функцию getClaimableAmount, чтобы определить, сколько токенов доступно для клейма.
# 5. Клейм токенов:
# • Программа вызывает функцию claim, передавая количество токенов для клейма (например, по 5 токенов за раз).
# • Клеймить можно несколько раз, пока не будут получены все доступные токены (максимум 25 токенов).
# • Если попытка клеймить превышает доступное количество токенов, программа выводит сообщение и прекращает выполнение.
# 6. Обработка транзакций:
# • Программа сохраняет хэши транзакций и ожидает их подтверждения.
# • После каждой успешной транзакции выводится сообщение об успешном клейме токенов.
# • После получения всех 25 токенов программа уведомляет пользователя о невозможности дальнейшего клейма.

import asyncio

from client import Client
from settings import PRIVATE_KEY, PROXY
from networks import get_network_by_name
from modules.bridges.stargate import StargateV2


async def main() -> None:
    """
    Stargate V2 TAXI/BUS bridge (Arbitrum and Optimism chains only)
    !CAUTION!
    On stargate frontend they use Stargate V1 contracts, not V2.
    """
    
    SRC_TOKEN: str = 'USDC' # ETH -> ETH, USDC -> USDC
    SRC_CHAIN: str = 'Optimism'
    DST_TOKEN: str = 'USDC' # ETH -> ETH, USDC -> USDC
    DST_CHAIN: str = 'Arbitrum'
    AMOUNT: float = 0.199994
    SLIPPAGE: float = 0.5 # 0.5 = 0.5%, 2 = 2%
    BRIDGE_MODE: str = 'TAXI' # "TAXI" - fast and expensive, "BUS" - slow and cheap
    
    client = Client(
        account_name="aiostudy", 
        network=get_network_by_name(SRC_CHAIN),
        private_key=PRIVATE_KEY,
        proxy=PROXY,
    )
    
    async with client:
        stargate_v2 = StargateV2(client=client)
        await stargate_v2.bridge(
            src_token_name=SRC_TOKEN,
            src_chain=get_network_by_name(SRC_CHAIN),
            dst_token_name=DST_TOKEN,
            dst_chain=get_network_by_name(DST_CHAIN),
            amount_to_bridge_ether=AMOUNT,
            bridge_mode=BRIDGE_MODE, 
            slippage=SLIPPAGE
        )

if __name__ == "__main__":
    asyncio.run(main())
