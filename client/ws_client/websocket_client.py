import asyncio
import json

import websockets

from ws_client.websocket_handler import WebsocketHandler


class WebsocketClient:
    def __init__(self, uri, interval=1):
        self.interval = interval
        self.uri = uri
        self.handlers: list[WebsocketHandler] = []

    def add_handler(self, handler: WebsocketHandler):
        if handler not in self.handlers:
            self.handlers.append(handler)
        else:
            raise ValueError(f"Handler {handler} already exists")

    def remove_handler(self, handler: WebsocketHandler):
        if handler in self.handlers:
            self.handlers.remove(handler)
        else:
            raise ValueError(f"Handler {handler} not found")

    async def handle_message(self, ws, message):
        for handler in self.handlers:
            await handler.on_message(ws, json.loads(message))

    async def run(self):
        """启动客户端，接收和处理消息"""
        websocket = await websockets.connect(self.uri)
        print(f"Connected to {self.uri}")
        for handler in self.handlers:
            await handler.on_connected(websocket)
        try:
            async for message in websocket:
                print(f"Message received: {message}")
                asyncio.create_task(self.handle_message(websocket, message))
        except websockets.exceptions.ConnectionClosed:
            print("Connection closed")
        finally:
            for handler in self.handlers:
                await handler.on_disconnected(websocket)
            await websocket.close()
            print("Disconnected")
