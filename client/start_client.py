import asyncio

from ws_client.hearbeat_service import HeartbeatService
from ws_client.websocket_client import WebSocketClient


async def run():
    ws_client = WebSocketClient('ws://localhost:3940')
    ws_client.add_handler(HeartbeatService())

    ws_task = asyncio.create_task(ws_client.run())

    await asyncio.gather(ws_task)


if __name__ == '__main__':
    asyncio.run(run())
