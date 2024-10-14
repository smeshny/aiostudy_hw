# Напишите софт, с помощью которого можно отправлять весь баланс ERC20 токена в выбранной сети с одного кошелька 
# на другой (ERC20 токен = не нативный токен, то есть USDT, ARB, DAI, ZRO и все другие).

# PS: Сначала нужно получить баланс токена, который мы будем трансферить. 

# Требования:

# Возможность выбора сети (eth, bsc, arbitrum и тд) Возможность выбора токена Проверка статуса транзакции

# Дополнительные требование (не обязательные):

# Сделать возможность трансферить как весь баланс, так и только конкретное количество монет



import asyncio

from client import Client
from settings import NETWORK_TO_WORK, PRIVATE_KEY, TO_ADDRESS, VALUE_TO_SEND, TOKEN_TO_SEND


async def main() -> None:
    client = Client(
        account_name="aiostudy", 
        network=NETWORK_TO_WORK,
        private_key=PRIVATE_KEY, 
    )

    await client.transfer_erc20_token(
        token=TOKEN_TO_SEND,
        amount_to_transfer_ether=VALUE_TO_SEND,
        to_address=TO_ADDRESS,
    )

if __name__ == "__main__":
    asyncio.run(main())
