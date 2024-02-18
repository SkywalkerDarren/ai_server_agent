import asyncio

import aiohttp

from conf.config import CONFIG


class KookClient:
    BASE_URL = 'https://www.kookapp.cn'
    HEADER = {
        'Authorization': f'Bot {CONFIG.kook.token}',
        'Accept-Language': 'en-US',
        'Content-Type': 'application/json',
    }

    def __init__(self):
        self.guild_id = CONFIG.kook.guild_id
        self.sn = 0

    async def guild_list(self):
        url = f'{self.BASE_URL}/api/v3/guild/list'
        async with aiohttp.ClientSession() as session:
            async with session.get(url, headers=self.HEADER) as response:
                data = await response.json()
                return data['data']

    async def channel_list(self, guild_id: str):
        url = f'{self.BASE_URL}/api/v3/channel/list'
        async with aiohttp.ClientSession() as session:
            async with session.get(url, headers=self.HEADER, params={'guild_id': guild_id}) as response:
                data = await response.json()
                return data['data']

    async def me(self):
        url = f'{self.BASE_URL}/api/v3/user/me'
        async with aiohttp.ClientSession() as session:
            async with session.get(url, headers=self.HEADER) as response:
                data = await response.json()
                return data['data']

    async def user_view(self, user_id: str, guild_id: str):
        url = f'{self.BASE_URL}/api/v3/user/view'
        async with aiohttp.ClientSession() as session:
            async with session.get(url, headers=self.HEADER, params={'user_id': user_id, 'guild_id': guild_id}) as response:
                data = await response.json()
                return data['data']

    async def guild_role_list(self, guild_id: str):
        url = f'{self.BASE_URL}/api/v3/guild-role/list'
        async with aiohttp.ClientSession() as session:
            async with session.get(url, headers=self.HEADER, params={'guild_id': guild_id}) as response:
                data = await response.json()
                return data['data']

    async def create_message(self, channel_id: str, content: str):
        url = f'{self.BASE_URL}/api/v3/message/create'
        async with aiohttp.ClientSession() as session:
            async with session.post(url, headers=self.HEADER, json={'target_id': channel_id, 'content': content}) as response:
                data = await response.json()
                print(data)
                return data['data']

    async def get_gateway(self) -> dict:
        url = f'{self.BASE_URL}/api/v3/gateway/index'
        async with aiohttp.ClientSession() as session:
            async with session.get(url, headers=self.HEADER) as response:
                data = await response.json()
                return data['data']
