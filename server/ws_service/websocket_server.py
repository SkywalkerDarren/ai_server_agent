import websockets
from websockets import WebSocketServerProtocol

from ws_service.websocket_handler import WebsocketHandler


class WebSocketServer:
    def __init__(self, host='localhost', port=3940):
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

    async def handler(self, websocket: WebSocketServerProtocol):
        """处理客户端连接和心跳"""
        print(f"Client connected: {websocket.remote_address}")
        for handler in self.handlers:
            await handler.on_connected(websocket)
        try:
            async for message in websocket:
                print(f"Message received: {message}")
                for handler in self.handlers:
                    await handler.on_message(websocket, message)
                print(f"Message from client: {message}")
        except websockets.exceptions.ConnectionClosed as e:
            print(f"Client disconnected: {e.reason}")
        finally:
            for handler in self.handlers:
                await handler.on_disconnected(websocket)
            print(f"Client disconnected: {websocket.remote_address}")

    async def start(self):
        """启动WebSocket服务器"""
        self.server = await websockets.serve(self.handler, self.host, self.port)
        print(f"WebSocket Server started at ws://{self.host}:{self.port}")
        await self.server.wait_closed()

    async def stop(self):
        """停止WebSocket服务器"""
        self.server.close()
        await self.server.wait_closed()
        print("WebSocket Server stopped")