import json

from conf.config import CONFIG
from kook_bot.websocket_handler import WebsocketHandler


class AtMessageHandler(WebsocketHandler):

    def __init__(self, kook_client):
        self.kook_client = kook_client

    async def on_connected(self, websocket):
        pass

    async def on_message(self, websocket, message):
        start_met = f'(met){CONFIG.kook_uid}(met)'
        start_role = f'(rol){CONFIG.kook_role_id}(rol)'
        if message['channel_type'] == 'GROUP' and message['target_id'] == CONFIG.kook_channel_id:
            if message['content'].startswith(start_met):
                content = message['content'][len(start_met):].strip()
            elif message['content'].startswith(start_role):
                content = message['content'][len(start_role):].strip()
            else:
                content = None
            if not content:
                return

            if content.startswith('/'):
                if content == '/启动服务器':
                    from ali_service.ali_client import AliClient
                    ali = AliClient()
                    status = await ali.start_server()
                    if status:
                        await self.kook_client.create_message(CONFIG.kook_channel_id, f'服务器启动成功，ip地址：{status.public_ip}')
                    else:
                        await self.kook_client.create_message(CONFIG.kook_channel_id, '服务器启动失败')
                elif content == '/关闭服务器':
                    from ali_service.ali_client import AliClient
                    ali = AliClient()
                    stop_success = await ali.stop_server()
                    if stop_success:
                        await self.kook_client.create_message(CONFIG.kook_channel_id, '服务器关闭成功')
                    else:
                        await self.kook_client.create_message(CONFIG.kook_channel_id, '服务器关闭失败')
                else:
                    await self.kook_client.create_message(CONFIG.kook_channel_id, '不支持的命令，当前支持的命令有：/启动服务器、/关闭服务器')

            else:
                from ai_service.ai import AI
                ai = AI()
                ai_response = await ai.chat(content)
                print(f'ai: {ai_response}')
                response = await self.kook_client.create_message(CONFIG.kook_channel_id, ai_response)
                print(response)

    async def on_disconnected(self, websocket):
        pass