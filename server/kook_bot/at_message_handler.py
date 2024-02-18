from ai_service.ai import AI
from ali_service.ali_client import AliClient
from conf.config import CONFIG
from kook_bot.kook_client import KookClient
from kook_bot.websocket_handler import WebsocketHandler
from ws_service.message_service import MessageService


class AtMessageHandler(WebsocketHandler):

    def __init__(self, kook_client: KookClient, message_service: MessageService, ali_client: AliClient, ai_client: AI):
        self.kook_client = kook_client
        self.message_service = message_service
        self.ali_client = ali_client
        self.ai_client = ai_client

    async def on_connected(self, websocket):
        pass

    async def on_message(self, websocket, message):
        start_met = f'(met){CONFIG.kook.uid}(met)'
        start_role = f'(rol){CONFIG.kook.role_id}(rol)'
        if message['channel_type'] == 'GROUP' and message['target_id'] == CONFIG.kook.channel_id:
            if message['content'].startswith(start_met):
                content = message['content'][len(start_met):].strip()
            elif message['content'].startswith(start_role):
                content = message['content'][len(start_role):].strip()
            else:
                content = None
            if not content:
                return

            print(f'content: {content}')

            if content.startswith('/'):
                if content == '/启动服务器':
                    status = await self.ali_client.start_server()
                    if status:
                        await self.kook_client.create_message(CONFIG.kook.channel_id, f'服务器启动成功，ip地址：{status.public_ip}')
                    else:
                        await self.kook_client.create_message(CONFIG.kook.channel_id, '服务器启动失败')
                elif content == '/关闭服务器':
                    stop_success = await self.ali_client.stop_server()
                    if stop_success:
                        await self.kook_client.create_message(CONFIG.kook.channel_id, '服务器关闭成功')
                    else:
                        await self.kook_client.create_message(CONFIG.kook.channel_id, '服务器关闭失败')
                elif content == '/系统信息':
                    system_info = await self.message_service.get_system_info()
                    await self.kook_client.create_message(CONFIG.kook.channel_id, f'系统信息：{system_info}')
                elif content == '/echo':
                    resp = await self.kook_client.create_message(CONFIG.kook.channel_id, 'echo')
                    print(f'echo response: {resp}, {CONFIG.kook.channel_id}')
                else:
                    await self.kook_client.create_message(CONFIG.kook.channel_id, '不支持的命令')

            else:
                ai_response = await self.ai_client.chat(content)
                print(f'ai: {ai_response}')
                response = await self.kook_client.create_message(CONFIG.kook.channel_id, ai_response)
                print(f"kook response: {response}")

    async def on_disconnected(self, websocket):
        pass