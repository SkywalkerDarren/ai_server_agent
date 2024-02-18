import asyncio
import json

import websockets
from websockets import WebSocketServerProtocol

from ws_service.websocket_handler import WebsocketHandler


class WebSocketServer:
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.server = None
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

    async def handler(self, websocket: WebSocketServerProtocol):
        """处理客户端连接和心跳"""
        print(f"Client connected: {websocket.remote_address}")
        for handler in self.handlers:
            await handler.on_connected(websocket)
        try:
            async for message in websocket:
                print(f"Message received: {message}")
                asyncio.create_task(self.handle_message(websocket, message))
        except websockets.exceptions.ConnectionClosed as e:
            print(f"Client disconnected: {e.reason}")
        finally:
            for handler in self.handlers:
                await handler.on_disconnected(websocket)
            print(f"Client disconnected: {websocket.remote_address}")

    async def start(self):
        """启动WebSocket服务器"""
        try:
            self.server = await websockets.serve(self.handler, self.host, self.port)
            print(f"WebSocket Server started at ws://{self.host}:{self.port}")
            await self.server.wait_closed()
        except asyncio.CancelledError:
            print("WebSocket Server cancellation detected, stopping...")
            await self.stop()

    async def stop(self):
        """停止WebSocket服务器"""
        self.server.close()
        await self.server.wait_closed()
        print("WebSocket Server stopped")
