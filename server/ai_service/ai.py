import json

import tiktoken
from openai import AsyncOpenAI

from ai_service.tools import ServerSystemInfoTool, RunningGameTool, GameListTool, StartGameTool, StopGameTool, \
    StartServerTool, StopServerTool, ServerStatusTool
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
        self.tool_list = [
            ServerSystemInfoTool(self.message_service),
            RunningGameTool(self.message_service),
            GameListTool(self.message_service),
            StartGameTool(self.message_service),
            StopGameTool(self.message_service),
            StartServerTool(self.ali_client),
            StopServerTool(self.ali_client),
            ServerStatusTool(self.ali_client),
        ]
        self.system_prompt = "你是一个服务器智能助手，你可以作为聊天机器人回答用户的问题，你也可以使用各种工具来操作服务器，但是一次你只能操作一个工具。"
        self.history = []

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
                    "content": self.system_prompt
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
            tools=[t.get_info() for t in self.tool_list]
        )
        if response.choices[0].message.tool_calls:
            msg = ""
            tools = response.choices[0].message.tool_calls
            for tool in tools:
                msg += f"使用工具: {tool.function.name}\n"
                use_tool = next((t for t in self.tool_list if t.name == tool.function.name), None)
                observer = await use_tool.execute(json.loads(tool.function.arguments))
                msg += f"观察结果: {observer}\n"
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
        content = response.choices[0].message.content
        messages.append({
            'role': 'assistant',
            'content': content
        })
        self.history += messages[1:]
        return content
