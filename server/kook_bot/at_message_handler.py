from kook_bot.websocket_handler import WebsocketHandler


class AtMessageHandler(WebsocketHandler):
    async def on_connected(self, websocket):
        pass

    async def on_message(self, websocket, message):
        pass

    async def on_disconnected(self, websocket):
        pass