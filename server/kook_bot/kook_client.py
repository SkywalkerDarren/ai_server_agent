from conf.config import CONFIG
from kook_bot.websocket_handler import WebsocketHandler

import json
import zlib

import aiohttp
import asyncio
import websockets


class KookClient:
    BASE_URL = 'https://www.kookapp.cn'
    HEADER = {
        'Authorization': f'Bot {CONFIG.kook_token}',
        'Accept-Language': 'en-US',
        'Content-Type': 'application/json',
    }

    def __init__(self):
        self.guild_id = CONFIG.kook_guild_id
        self.sn = 0
        self.session_id = None
        self.interval = 30
        self.timeout = 6
        self.last_pong_time = 0
        self.timeout_task = None
        self.handlers: list[WebsocketHandler] = []

    def add_handler(self, handler):
        self.handlers.append(handler)

    async def guild_list(self):
        url = f'{self.BASE_URL}/api/v3/guild/list'
        async with aiohttp.ClientSession() as session:
            async with session.get(url, headers=self.HEADER) as response:
                data = await response.json()
                return data['data']

    async def channel_list(self):
        url = f'{self.BASE_URL}/api/v3/channel/list'
        async with aiohttp.ClientSession() as session:
            async with session.get(url, headers=self.HEADER, params={'guild_id': self.guild_id}) as response:
                data = await response.json()
                return data['data']

    async def get_gateway(self) -> str:
        url = f'{self.BASE_URL}/api/v3/gateway/index'
        i = 0
        while True:
            try:
                async with aiohttp.ClientSession() as session:
                    async with session.get(url, headers=self.HEADER) as response:
                        data = await response.json()
                        return data['data']['url']
            except Exception as e:
                print(f'Failed to get gateway', e)
                await asyncio.sleep(min(2 ** i, 60))

    async def heartbeat(self, ws: websockets.WebSocketClientProtocol):
        while ws.open:
            await ws.send(json.dumps({"s": 2, "sn": self.sn}))
            print(f'ping {self.sn}')
            self.timeout_task = asyncio.create_task(self.check_timeout(ws))
            await asyncio.sleep(self.interval)

    async def resume(self, ws: websockets.WebSocketClientProtocol):
        await ws.send(json.dumps({"s": 4, "sn": self.sn}))

    async def check_timeout(self, ws: websockets.WebSocketClientProtocol):
        await asyncio.sleep(self.timeout)
        print("Heartbeat timeout, disconnecting...")
        await ws.close()

    def update_pong_time(self):
        self.last_pong_time = asyncio.get_event_loop().time()

    async def start(self):
        while True:
            try:
                url = await self.get_gateway()

                max_connect_retry = 3
                for i in range(max_connect_retry):
                    try:
                        ws = await websockets.connect(url)
                        if ws.open:
                            print(f'Connected to {url}')
                            break
                    except Exception as e:
                        print(f'Failed to connect to {url}', e)
                        await asyncio.sleep(2 ** i)
                else:
                    print(f'Failed to connect to {url} after {max_connect_retry} retries')
                    continue

                for handler in self.handlers:
                    await handler.on_connected(ws)

                self.sn = 0
                self.session_id = None
                self.timeout_task = asyncio.create_task(self.check_timeout(ws))

                while True:
                    message = await ws.recv()
                    message = zlib.decompress(message).decode('utf-8')
                    message = json.loads(message)

                    print(f"Message received: {message}")

                    if message['s'] == 1:
                        print('hello')
                        self.session_id = message['d']['session_id']
                        if self.timeout_task and not self.timeout_task.done():
                            self.timeout_task.cancel()  # 取消超时检测任务
                            asyncio.create_task(self.heartbeat(ws))
                    elif message['s'] == 3:
                        print('pong')
                        if self.timeout_task and not self.timeout_task.done():
                            self.timeout_task.cancel()  # 取消超时检测任务
                    elif message['s'] == 5:
                        print('reconnect')
                        break
                    elif message['s'] == 6:
                        print('resume ack')
                    elif message['s'] == 0:
                        self.sn = message['sn']
                        print('dispatch event')
                        for handler in self.handlers:
                            await handler.on_message(ws, message)
            except Exception as e:
                print('Error:', e)
                continue
