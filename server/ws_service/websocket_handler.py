import abc
from typing import TypeVar

from websockets import WebSocketServerProtocol


class WebsocketHandler(abc.ABC):

    @abc.abstractmethod
    async def on_connected(self, websocket: WebSocketServerProtocol):
        pass

    @abc.abstractmethod
    async def on_message(self, websocket: WebSocketServerProtocol, message: dict):
        pass

    @abc.abstractmethod
    async def on_disconnected(self, websocket: WebSocketServerProtocol):
        pass
