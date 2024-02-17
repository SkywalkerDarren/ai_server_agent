import json

import psutil
from websockets import WebSocketClientProtocol

from ws_client.websocket_handler import WebsocketHandler


class MessageService(WebsocketHandler):
    async def on_connected(self, websocket: WebSocketClientProtocol):
        pass

    async def get_system_info(self) -> dict:
        cpu_usage = psutil.cpu_percent()
        mem_usage = psutil.virtual_memory().percent
        return {
            "type": "system_info",
            "data": {
                "cpu_usage": cpu_usage,
                "mem_usage": mem_usage
            }
        }

    async def get_running_games(self):
        # TODO implement this
        return {
            "type": "running_games",
            "data": {
                "games": []
            }
        }

    async def get_game_list(self):
        # TODO implement this
        return {
            "type": "game_list",
            "data": {
                "games": [
                    "幻兽帕鲁",
                    "异星工厂",
                    "英灵神殿",
                ]
            }
        }

    async def start_game(self, game: str):
        # TODO implement this
        return {
            "type": "start_game",
            "data": {
                "status": "success"
            }
        }

    async def stop_game(self, game: str):
        # TODO implement this
        return {
            "type": "stop_game",
            "data": {
                "status": "success"
            }
        }

    async def on_message(self, websocket: WebSocketClientProtocol, message: dict):
        message_type = message['type']
        if message_type == "system_info":
            response = await self.get_system_info()
        elif message_type == "running_games":
            response = await self.get_running_games()
        elif message_type == "game_list":
            response = await self.get_game_list()
        elif message_type == "start_game":
            response = await self.start_game(message['data']['game'])
        elif message_type == "stop_game":
            response = await self.stop_game(message['data']['game'])
        else:
            return

        msg_id = message['msg_id']
        response['msg_id'] = msg_id
        if websocket.open:
            try:
                await websocket.send(json.dumps(response))
            except Exception as e:
                print(f'Error sending message: {e}')

    async def on_disconnected(self, websocket: WebSocketClientProtocol):
        pass
