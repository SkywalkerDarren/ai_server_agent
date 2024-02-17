import asyncio

from ws_client.hearbeat_service import HeartbeatService
from ws_client.message_service import MessageService
from ws_client.websocket_client import WebsocketClient


async def run():
    ws_client = WebsocketClient('ws://localhost:39401')
    ws_client.add_handler(HeartbeatService())
    msg_service = MessageService()
    ws_client.add_handler(msg_service)

    ws_task = asyncio.create_task(ws_client.run())

    await asyncio.gather(ws_task)


if __name__ == '__main__':
    asyncio.run(run())
