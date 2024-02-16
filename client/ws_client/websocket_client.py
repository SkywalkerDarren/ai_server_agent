import json

import websockets

from ws_client.websocket_handler import WebsocketHandler


class WebSocketClient:
    def __init__(self, uri, interval=1):
        self.interval = interval
        self.uri = uri
        self.websocket = None
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

    async def run(self):
        """启动客户端，接收和处理消息"""
        self.websocket = await websockets.connect(self.uri)
        print(f"Connected to {self.uri}")
        for handler in self.handlers:
            await handler.on_connected(self.websocket)
        try:
            # 持续监听和处理消息
            while True:
                msg = await self.websocket.recv()
                print(f"Message received: {msg}")
                for handler in self.handlers:
                    await handler.on_message(self.websocket, msg)
                print(f"Message from server: {msg}")
        except websockets.exceptions.ConnectionClosed:
            print("Connection closed")
        finally:
            for handler in self.handlers:
                await handler.on_disconnected(self.websocket)
            await self.websocket.close()
            print("Disconnected")
