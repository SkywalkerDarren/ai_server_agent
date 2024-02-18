from conf.config import CONFIG
from kook_bot.at_message_handler import AtMessageHandler
from kook_bot.kook_client import KookClient
from kook_bot.websocket_handler import WebsocketHandler

import json
import zlib

import asyncio
import websockets


class KookWebsocket:

    def __init__(self, kook_client):
        self.kook_client = kook_client
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

    async def handle_message(self, ws, message):
        for handler in self.handlers:
            await handler.on_message(ws, message['d'])

    async def start(self):
        ws = None
        while True:
            try:
                i = 0
                while True:
                    try:
                        url = (await self.kook_client.get_gateway())['url']
                        break
                    except asyncio.CancelledError as e:
                        print(f'Cancelled', e)
                        raise e
                    except Exception as e:
                        print(f'Failed to get gateway', e)
                        await asyncio.sleep(min(2 ** i, 60))

                max_connect_retry = 3
                for i in range(max_connect_retry):
                    try:
                        ws = await websockets.connect(url)
                        if ws.open:
                            print(f'Connected to {url}')
                            break
                    except asyncio.CancelledError as e:
                        if ws and ws.open:
                            await ws.close()
                        print(f'Cancelled', e)
                        raise e
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
                        asyncio.create_task(self.handle_message(ws, message))
            except asyncio.CancelledError as e:
                if ws and ws.open:
                    await ws.close()
                print(f'Cancelled', e)
                raise e
            except Exception as e:
                print('Error:', e)
                continue
