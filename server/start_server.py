import asyncio

from ai_service.ai import AI
from ali_service.ali_client import AliClient
from kook_bot.at_message_handler import AtMessageHandler
from kook_bot.kook_client import KookClient
from kook_bot.kook_websocket import KookWebsocket
from search_service.search_client import SearchClient
from search_service.search_service import SearchService
from ws_service.hearbeat_service import HeartbeatService
from ws_service.message_service import MessageService
from ws_service.websocket_server import WebSocketServer
import argparse


def cli():
    args = argparse.ArgumentParser()
    args.add_argument("--host", type=str, default="localhost")
    args.add_argument("--port", type=int, default=39401)
    return args.parse_args()


async def run():
    args = cli()

    ws_server = WebSocketServer(args.host, args.port)
    ws_server.add_handler(HeartbeatService())
    msg_service = MessageService()
    ws_server.add_handler(msg_service)
    ws_task = asyncio.create_task(ws_server.start())

    ali_client = AliClient()

    search_service = SearchService()

    ai_client = AI(msg_service, ali_client, search_service)

    kook_client = KookClient()
    kook_websocket = KookWebsocket(kook_client)
    kook_websocket.add_handler(AtMessageHandler(kook_client, msg_service, ali_client, ai_client))
    kook_task = asyncio.create_task(kook_websocket.start())

    print(f'ws server start at {args.host}:{args.port}')
    await asyncio.gather(ws_task, kook_task)


if __name__ == '__main__':
    asyncio.run(run())
