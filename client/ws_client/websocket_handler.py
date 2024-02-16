import abc
from websockets import WebSocketClientProtocol



class WebsocketHandler(abc.ABC):
    @abc.abstractmethod
    async def on_connected(self, websocket: WebSocketClientProtocol):
        pass

    @abc.abstractmethod
    async def on_message(self, websocket: WebSocketClientProtocol, message: str):
        pass

    @abc.abstractmethod
    async def on_disconnected(self, websocket: WebSocketClientProtocol):
        pass
