import asyncio
import random

from client import Client
from settings import CAPMONSTER_API_KEY


class CapMonsterSolver:
    def __init__(self, client: Client, task_type: str, website_url: str, website_key: str) -> None:
        self.client: Client = client
        self.task_type = task_type
        self.website_url = website_url
        self.website_key = website_key


    async def create_task_for_captcha(self):
        url = 'https://api.capmonster.cloud/createTask'

        payload = {
            "clientKey": CAPMONSTER_API_KEY,
            "task": {
                "type": self.task_type,
                "websiteURL": self.website_url,
                "websiteKey": self.website_key,
                "proxyType": "http",
                "proxyAddress": self.client.proxy_address,
                "proxyPort": self.client.proxy_port,
                "proxyLogin": self.client.proxy_login,
                "proxyPassword": self.client.proxy_password,
                "userAgent": self.client.user_agent,
            },
        }

        response = await self.client.make_request(method='POST', url=url, json=payload)

        if response['errorId'] == 0:
            return response['taskId']
        
        raise RuntimeError(f'Failed to create captcha task. Error id: {response["errorId"]}')
    
    async def get_captcha_solution(self, task_id: str) -> str:
        url = 'https://api.capmonster.cloud/getTaskResult'

        payload = {
            "clientKey": CAPMONSTER_API_KEY,
            "taskId": task_id
            }
        
        total_time = 0
        timeout = 360
        while total_time < timeout:
            response = await self.client.make_request(method='POST', url=url, json=payload)
            if response['status'] == 'ready':
                return response['solution']['gRecaptchaResponse']
            total_time += 5
            await asyncio.sleep(5)
            if total_time >= timeout:
                raise RuntimeError(f'Failed to get captcha solution in {timeout} seconds')
            