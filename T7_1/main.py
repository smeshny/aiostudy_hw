# Задание от преподавателя

# Напишите софт, с помощью которого можно отправлять нативный токен в выбранной сети с одного кошелька на другой.
# Требования:

#     Нужно указать количество нативного токена, которое будем трансферить
#     Проверка статуса транзакции
#     Возможность выбора сети (eth, bsc, arbitrum и тд)

# ⚠️ Внимание! Следующие дополнительные требования применяются ко всем последующим домашним работам. В основном они не обязательны, но лучше чтобы вы их придерживались.

#     Использование ООП
#     Использование asyncio
#     Использование EIP-1559 транзакций 



import asyncio

from client import Client
from settings import NETWORK_TO_WORK, PRIVATE_KEY, TO_ADDRESS, VALUE_TO_SEND


async def main() -> None:
    client = Client(
        account_name="aiostudy", 
        network=NETWORK_TO_WORK,
        private_key=PRIVATE_KEY, 
    )

    await client.transfer_native_token(VALUE_TO_SEND, TO_ADDRESS)

if __name__ == "__main__":
    asyncio.run(main())
