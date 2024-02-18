import json
import asyncio

from websockets import WebSocketClientProtocol

from ws_client.websocket_handler import WebsocketHandler


class HeartbeatService(WebsocketHandler):
    def __init__(self, interval=30, timeout=10):
        self.timeout = timeout
        self.interval = interval
        self.heartbeat_task = None
        self.timeout_task = None

    async def on_connected(self, websocket: WebSocketClientProtocol):
        self.heartbeat_task = asyncio.create_task(self.send_heartbeat(websocket))
        print(f"connected to {websocket.remote_address}")

    async def on_message(self, websocket: WebSocketClientProtocol, message):
        """处理心跳消息"""
        if message['type'] == "heartbeat_ack":
            data = message['data']
            rtt = asyncio.get_event_loop().time() - data['timestamp']
            print(f"Heartbeat received: {rtt}")
            if self.timeout_task and not self.timeout_task.done():
                self.timeout_task.cancel()  # 取消超时检测任务

    async def on_disconnected(self, websocket: WebSocketClientProtocol):
        await self.stop()

    async def check_timeout(self, ws: WebSocketClientProtocol):
        await asyncio.sleep(self.timeout)
        print("Heartbeat timeout, disconnecting...")
        await ws.close()

    async def send_heartbeat(self, websocket: WebSocketClientProtocol):
        """发送心跳消息"""
        while True:
            data = {
                'type': "heartbeat",
                'data': {
                    'timestamp': asyncio.get_event_loop().time()
                }
            }
            await websocket.send(json.dumps(data))
            self.timeout_task = asyncio.create_task(self.check_timeout(websocket))
            await asyncio.sleep(self.interval)

    async def stop(self):
        """停止心跳服务"""
        print("Stopping heartbeat service...")
        if self.heartbeat_task:
            try:
                self.heartbeat_task.cancel()
                await self.heartbeat_task
            except asyncio.CancelledError:
                pass

        if self.timeout_task:
            try:
                self.timeout_task.cancel()
                await self.timeout_task
            except asyncio.CancelledError:
                pass
