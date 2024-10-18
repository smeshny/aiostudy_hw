# Реализуйте решение капчи через сервис CapMonster на кране от проекта Movement (EVM) и клейм токенов MOVE. 
# Капча на сайте решается на интефейсе, а не под капотом и является reCaptchaV2.
# CapMonster имеет отличную документацию для работы с любим типом капчи, не стесняйтесь пользоваться ей. 
# В конечном итоге токены MOVE должны оказаться на вашем EVM кошельке Сайт FaucetДокументация CapMonsterП
# одсказка 1. Решенную капчу нужно передавать в хедерсы запроса.

# Подсказка 2. Внимательно изучите payload запроса на получение токенов.

# Подсказка 3. Server error - фасету плохо, попробуйте позже

import asyncio

from client import Client
from modules.movement_faucet import MovementFaucet
from settings import NETWORK_TO_WORK, PRIVATE_KEY, TO_ADDRESS, VALUE_TO_SEND, TOKEN_TO_SEND, \
                     PROXY       


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
