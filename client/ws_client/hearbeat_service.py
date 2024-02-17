import json
import asyncio

from websockets import WebSocketClientProtocol

from ws_client.websocket_handler import WebsocketHandler


class HeartbeatService(WebsocketHandler):
    def __init__(self, interval=3, timeout=30):
        self.timeout = timeout
        self.interval = interval
        self.last_heartbeat = 0
        self.heartbeat_task = None
        self.timeout_task = None

    async def on_connected(self, websocket: WebSocketClientProtocol):
        self.last_heartbeat = asyncio.get_event_loop().time()
        self.timeout_task = asyncio.create_task(self.check_timeout(websocket))
        self.heartbeat_task = asyncio.create_task(self.send_heartbeat(websocket))
        print(f"connected to {websocket.remote_address}")

    async def on_message(self, websocket: WebSocketClientProtocol, message):
        """处理心跳消息"""
        if message['type'] == "heartbeat_ack":
            data = message['data']
            rtt = asyncio.get_event_loop().time() - data['timestamp']
            print(f"Heartbeat received: {rtt}")
            self.last_heartbeat = asyncio.get_event_loop().time()  # 更新收到心跳的时间

    async def on_disconnected(self, websocket: WebSocketClientProtocol):
        await self.stop()

    async def check_timeout(self, websocket: WebSocketClientProtocol):
        """检查心跳超时"""
        while True:
            await asyncio.sleep(1)  # 定期检查
            if asyncio.get_event_loop().time() - self.last_heartbeat > self.timeout:
                print("Heartbeat timeout, disconnecting...")
                await websocket.close()  # 主动断开连接
                break

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
