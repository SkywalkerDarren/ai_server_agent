import json

from websockets import WebSocketServerProtocol

from ws_service.websocket_handler import WebsocketHandler


class HeartbeatService(WebsocketHandler):
    def __init__(self, timeout=3):
        self.timeout = timeout

    async def on_connected(self, websocket: WebSocketServerProtocol):
        ...

    async def on_message(self, websocket: WebSocketServerProtocol, message: str):
        """处理心跳消息"""
        message = json.loads(message)
        if message['type'] == "heartbeat":
            resp = {
                "type": "heartbeat_ack",
                "data": {
                    "timestamp": message['data']["timestamp"]
                }
            }
            await websocket.send(json.dumps(resp))

    async def on_disconnected(self, websocket: WebSocketServerProtocol):
        ...
