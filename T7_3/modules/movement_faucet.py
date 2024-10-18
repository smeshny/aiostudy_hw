import asyncio

from client import Client
from modules.capmonster import CapMonsterSolver


class MovementFaucet:
    def __init__(self, client: Client) -> None:
        self.client: Client = client
        self.task_type = "RecaptchaV2Task"
        self.website_url = "https://faucet.movementlabs.xyz/"
        self.website_key = "6LdPgxMqAAAAAByFdD5V8PiPKYZS4mSZWUUcZW6B"
        self.faucet_requset_url = 'https://mevm.devnet.imola.movementlabs.xyz/'

    async def get_captcha_solution(self) -> str:
        capmonster_solver = CapMonsterSolver(
            client=self.client, task_type=self.task_type, website_url=self.website_url, website_key=self.website_key
            )
        captcha_id = await capmonster_solver.create_task_for_captcha()
        captcha_solution = await capmonster_solver.get_captcha_solution(captcha_id)
        return captcha_solution

    async def get_movement_tokens(self):
        token = await self.get_captcha_solution()
        headers = {
            "accept": "application/json, text/plain, */*",
            "accept-encoding": "gzip, deflate, br, zstd",
            "accept-language": "en-US,en;q=0.9",
            "cache-control": "no-cache",
            "content-type": "application/json",
            "origin": "https://faucet.movementlabs.xyz",
            "pragma": "no-cache",
            "priority": "u=1, i",
            "referer": "https://faucet.movementlabs.xyz/",
            "sec-ch-ua": '"Google Chrome";v="129", "Not=A?Brand";v="8", "Chromium";v="129"',
            "sec-ch-ua-mobile": "?0",
            "sec-ch-ua-platform": '"macOS"',
            "sec-fetch-dest": "empty",
            "sec-fetch-mode": "cors",
            "sec-fetch-site": "same-site",
            "token": token,
            "user-agent": self.client.user_agent
        }
        
        payload = {
            "jsonrpc": "2.0",
            "id": 1,
            "method": "eth_batch_faucet",
            "params": [self.client.address],
        }

        total_time = 0
        timeout = 500
        # {'jsonrpc': '2.0', 'id': 1, 'result': '0x2492a142512c47760765f1f85d7855af831ac059028e7bb86069bfe8f66945c5'}
        while total_time < timeout:
            response = await self.client.make_request(
                method='POST', url=self.faucet_requset_url, headers=headers, json=payload
                )
            if response['result']:
                print(f"Successfully received tokens! tx: {response['result']}")
                return response['result']
            total_time += 5
            await asyncio.sleep(5)
            if total_time >= timeout:
                raise RuntimeError(f'Failed to get Movements tokens in {timeout} seconds')
