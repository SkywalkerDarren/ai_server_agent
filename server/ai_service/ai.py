import json

import tiktoken
from openai import AsyncOpenAI

from ai_service.tools import ServerSystemInfoTool, RunningGameTool, GameListTool, StartGameTool, StopGameTool, \
    StartServerTool, StopServerTool, ServerStatusTool, CreateServerTool, SearchEngineTool
from ali_service.ali_client import AliClient
from conf.config import CONFIG
from search_service.search_service import SearchService
from ws_service.message_service import MessageService


class AI:
    def __init__(self, message_service: MessageService, ali_client: AliClient, search_service: SearchService):
        self.running_status = False
        self.last_message = ""
        self.message_service = message_service
        self.ali_client = ali_client
        self.search_service = search_service
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
            CreateServerTool(self.ali_client),
            StartServerTool(self.ali_client),
            StopServerTool(self.ali_client),
            ServerStatusTool(self.ali_client),
            SearchEngineTool(self.search_service),
        ]
        self.system_prompt = "你是一个非常幽默诙谐的服务器智能助手，你可以与用户进行聊天，你也可以使用各种工具来操作服务器，但是一次你只能操作一个工具。"
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
        system = [
            {
                "role": "system",
                "content": self.system_prompt
            }
        ]
        messages = [
                {
                    "role": "user",
                    "content": user_input
                }
            ]
        response = await self.client.chat.completions.create(
            n=1,
            model=self.model_name,
            messages=system + self.history + messages,
            tools=[t.get_info() for t in self.tool_list]
        )
        if response.choices[0].message.tool_calls:
            msg = ""
            tools = response.choices[0].message.tool_calls
            for tool in tools:
                msg += f"使用工具: {tool.function.name} {tool.function.arguments}\n"
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
        self.history += messages
        self.filter_history()
        return content

    def filter_history(self):
        tokens = 0
        max_tokens = 10240
        reserved_history = self.history[::-1]
        for i, msg in enumerate(reserved_history):
            tokens += len(self.token_model.encode(msg['content']))
            if tokens > max_tokens:
                self.history = self.history[-i:]
                break
