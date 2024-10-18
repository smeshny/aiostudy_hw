# Задание: Подписание и проверка типизированных сообщений

# Подпишите типизированное сообщение на сайте Uniswap и получите с него сигнатуру. 
# После этого проверьте, действительно ли данная сигнатура валидна для исходного сообщения. 

# Подсказка 1. Подпись инициализируется при свапах из НЕнативных токенов

import asyncio

from client import Client
from modules.movement_faucet import MovementFaucet
from settings import NETWORK_TO_WORK, PRIVATE_KEY, PROXY       


async def main() -> None:
    client = Client(
        account_name="aiostudy", 
        network=NETWORK_TO_WORK,
        private_key=PRIVATE_KEY,
        proxy=PROXY,
    )
    async with client:
        movement_faucet = MovementFaucet(client=client)
        await movement_faucet.get_movement_tokens()


if __name__ == "__main__":
    asyncio.run(main())
