import tiktoken
from openai import AsyncOpenAI

from ali_service.ali_client import AliClient
from conf.config import CONFIG
from ws_service.message_service import MessageService


class AI:
    def __init__(self, message_service: MessageService, ali_client: AliClient):
        self.running_status = False
        self.last_message = ""
        self.message_service = message_service
        self.ali_client = ali_client
        self.model_name = "gpt-3.5-turbo-0125"
        self.client = AsyncOpenAI(
            api_key=CONFIG.openai.token,
        )
        self.token_model = tiktoken.encoding_for_model(self.model_name)

    async def chat(self, user_input: str):
        if self.running_status:
            return f"正在处理消息：{self.last_message}"
        self.running_status = True
        self.last_message = user_input
        try:
            response = await self._chat(user_input)
            return response
        finally:
            self.running_status = False

    async def _chat(self, user_input: str):
        messages = [
                {
                    "role": "system",
                    "content": "你是一个服务器智能助手，你可以回答用户的问题，你也可以使用各种工具来操作服务器，但是一次你只能操作一个工具。"
                },
                {
                    "role": "user",
                    "content": user_input
                }
            ]
        response = await self.client.chat.completions.create(
            n=1,
            model=self.model_name,
            messages=messages,
            tools=[
                {
                    "type": "function",
                    "function": {
                        "name": "server_system_info",
                        "description": "查看服务器系统状态信息，包括cpu使用率和内存使用率",
                    }
                },
                {
                    "type": "function",
                    "function": {
                        "name": "running_games",
                        "description": "查看正在运行的游戏服务器列表",
                    }
                },
                {
                    "type": "function",
                    "function": {
                        "name": "game_list",
                        "description": "查看服务器支持运行的游戏服务器列表",
                    }
                },
                {
                    "type": "function",
                    "function": {
                        "name": "start_game",
                        "description": "根据游戏名启动服务器上的一个游戏服务器",
                        "parameters": {
                            "type": "object",
                            "required": [
                                "game"
                            ],
                            "properties": {
                                "game": {
                                    "type": "string",
                                    "description": "游戏名称"
                                }
                            }
                        }
                    }
                },
                {
                    "type": "function",
                    "function": {
                        "name": "stop_game",
                        "description": "根据游戏名停止服务器上的一个游戏服务器",
                        "parameters": {
                            "type": "object",
                            "required": [
                                "game"
                            ],
                            "properties": {
                                "game": {
                                    "type": "string",
                                    "description": "游戏名称"
                                }
                            }
                        }
                    }
                },
                {
                    "type": "function",
                    "function": {
                        "name": "start_server",
                        "description": "启动阿里云服务器",
                    },
                },
                {
                    "type": "function",
                    "function": {
                        "name": "stop_server",
                        "description": "停止阿里云服务器",
                    },
                },
                {
                    "type": "function",
                    "function": {
                        "name": "reboot_server",
                        "description": "重启阿里云服务器",
                    },
                },
                {
                    "type": "function",
                    "function": {
                        "name": "server_status",
                        "description": "查看阿里云服务器信息",
                    },
                }
            ]
        )
        if response.choices[0].message.tool_calls:
            msg = ""
            tools = response.choices[0].message.tool_calls
            for tool in tools:
                msg += f"使用工具: {tool.function.name}\n"
                if tool.function.name == "server_system_info":
                    system_info = await self.message_service.get_system_info()
                    msg += f"观察结果: {system_info}\n"
                elif tool.function.name == "running_games":
                    running_games = await self.message_service.get_running_games()
                    msg += f"观察结果: {running_games}\n"
                elif tool.function.name == "game_list":
                    game_list = await self.message_service.get_game_list()
                    msg += f"观察结果: {game_list}\n"
                elif tool.function.name == "start_game":
                    game = tool.parameters["game"]
                    is_success = await self.message_service.start_game(game)
                    msg += f"观察结果: {is_success}\n"
                elif tool.function.name == "stop_game":
                    game = tool.parameters["game"]
                    is_success = await self.message_service.stop_game(game)
                    msg += f"观察结果: {is_success}\n"
                elif tool.function.name == "start_server":
                    status = await self.ali_client.start_server()
                    msg += f"观察结果: {status}\n"
                elif tool.function.name == "stop_server":
                    status = await self.ali_client.stop_server()
                    msg += f"观察结果: {status}\n"
                elif tool.function.name == "server_status":
                    status = await self.ali_client.get_server_status(CONFIG.aliyun.server_name)
                    msg += f"观察结果: {status}\n"
            print(f'ai: {msg}')
            messages.append({
                'role': 'assistant',
                'content': msg
            })
            messages.append({
                'role': 'user',
                'content': '请根据观察结果进行回复。'
            })
            response = await self.client.chat.completions.create(
                n=1,
                model=self.model_name,
                messages=messages,
            )
        return response.choices[0].message.content
