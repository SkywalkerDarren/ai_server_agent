import asyncio

from ws_service.hearbeat_service import HeartbeatService
from ws_service.websocket_server import WebSocketServer


async def run():
    ws_server = WebSocketServer()
    ws_server.add_handler(HeartbeatService())
    ws_task = asyncio.create_task(ws_server.start())

    # kook_client = KookBot()
    # kook_task = asyncio.create_task(kook_client.start())

    await asyncio.gather(ws_task)


if __name__ == '__main__':
    asyncio.run(run())
