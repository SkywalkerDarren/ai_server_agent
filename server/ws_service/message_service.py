import asyncio
import json
import uuid

from websockets import WebSocketServerProtocol

from ws_service.websocket_handler import WebsocketHandler


class MessageService(WebsocketHandler):

    def __init__(self):
        self.ws = None
        self.futures = {}

    async def get_system_info(self) -> dict:
        req = {
            "type": "system_info",
            "data": {}
        }
        resp = await self._send_message(req)
        if not resp:
            return {}
        return resp['data']

    async def get_running_games(self) -> list[str]:
        req = {
            "type": "running_games",
            "data": {}
        }
        resp = await self._send_message(req)
        if not resp:
            return []
        return resp['data']['games']

    async def get_game_list(self) -> list[str]:
        req = {
            "type": "game_list",
            "data": {}
        }
        resp = await self._send_message(req)
        if not resp:
            return []
        return resp['data']['games']

    async def start_game(self, game: str) -> bool:
        req = {
            "type": "start_game",
            "data": {
                "game": game,
            }
        }
        resp = await self._send_message(req)
        if not resp:
            return False
        if resp['data']['status'] == "success":
            return True
        else:
            return False

    async def stop_game(self, game: str) -> bool:
        req = {
            "type": "stop_game",
            "data": {
                "game": game,
            }
        }
        resp = await self._send_message(req)
        if not resp:
            return False
        if resp['data']['status'] == "success":
            return True
        else:
            return False

    async def _send_message(self, message: dict):
        if not self.ws or not self.ws.open:
            print("WebSocket not connected")
            return

        msg_id = uuid.uuid4().hex
        message['msg_id'] = msg_id

        self.futures[msg_id] = asyncio.Future()

        try:
            await self.ws.send(json.dumps(message))
            return await asyncio.wait_for(self.futures[msg_id], timeout=6)
        except asyncio.TimeoutError:
            print(f"Message {msg_id} timeout")
            return None
        finally:
            del self.futures[msg_id]

    async def on_connected(self, websocket: WebSocketServerProtocol):
        self.ws = websocket
        pass

    async def on_message(self, websocket: WebSocketServerProtocol, message: dict):
        if message.get('msg_id') and message['msg_id'] in self.futures:
            future = self.futures[message['msg_id']]
            future.set_result(message)

    async def on_disconnected(self, websocket: WebSocketServerProtocol):
        self.ws = None
        pass
