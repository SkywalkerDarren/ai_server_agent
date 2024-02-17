import asyncio
import argparse

from ws_client.hearbeat_service import HeartbeatService
from ws_client.message_service import MessageService
from ws_client.websocket_client import WebsocketClient


def cli():
    args = argparse.ArgumentParser()
    args.add_argument('--url', default='ws://localhost:39401')
    return args.parse_args()


async def run():
    args = cli()

    ws_client = WebsocketClient(args.url)
    ws_client.add_handler(HeartbeatService())
    msg_service = MessageService()
    ws_client.add_handler(msg_service)

    ws_task = asyncio.create_task(ws_client.run())

    await asyncio.gather(ws_task)


if __name__ == '__main__':
    asyncio.run(run())
