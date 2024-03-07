import json
from dataclasses import asdict

from pydantic import BaseModel, ValidationError

from typing import Type, Optional


class BaseTool:
    def __init__(self, name, description, param_model: Type[BaseModel] = None):
        self.name = name
        self.description = description
        self.param_model = param_model

    async def execute(self, parameters: dict = None) -> str:
        if self.param_model and parameters:
            # 使用 pydantic 模型校验参数
            try:
                validated_params = self.param_model(**parameters)
            except ValidationError as e:
                raise ValueError(f"Parameter validation error: {e}")
        else:
            validated_params = None

        return await self.run(validated_params)

    async def run(self, validated_params: Optional[BaseModel]) -> str:
        raise NotImplementedError("This method should be implemented by subclasses.")

    def get_info(self):
        return {
            "type": "function",
            "function": {
                "name": self.name,
                "description": self.description,
                "parameters": self.param_model.model_json_schema() if self.param_model else None
            }
        }


class ServerSystemInfoTool(BaseTool):
    def __init__(self, message_service):
        self.message_service = message_service
        super().__init__("server_system_info", "查看服务器系统状态信息，包括cpu使用率和内存使用率")

    async def run(self, validated_params):
        status = await self.message_service.get_system_info()
        if not status:
            return "获取服务器状态信息失败"
        return json.dumps(status)


class RunningGameTool(BaseTool):
    def __init__(self, message_service):
        self.message_service = message_service
        super().__init__("running_game", "查看正在运行的游戏服务器列表")

    async def run(self, validated_params):
        running_games = await self.message_service.get_running_games()
        if not running_games:
            return "没有正在运行的游戏服务器"
        return json.dumps(running_games)


class GameListTool(BaseTool):
    def __init__(self, message_service):
        self.message_service = message_service
        super().__init__("game_list", "查看服务器支持运行的游戏服务器列表")

    async def run(self, validated_params):
        game_list = await self.message_service.get_game_list()
        if not game_list:
            return "服务器上没有游戏或服务器未启动"
        return json.dumps(game_list)


class StartGameTool(BaseTool):
    class StartGameParams(BaseModel):
        """
        游戏名称
        """
        game: str

    def __init__(self, message_service):
        self.message_service = message_service
        super().__init__("start_game", "根据游戏名启动服务器上的一个游戏服务器，要使用这个工具必须提到游戏名称",
                         self.StartGameParams)

    async def run(self, validated_params: StartGameParams):
        # 使用已校验和转换过的参数
        game = validated_params.game
        is_success = await self.message_service.start_game(game)
        if is_success:
            return "启动游戏服务器成功"
        else:
            return "启动游戏服务器失败"


class StopGameTool(BaseTool):
    class StopGameParams(BaseModel):
        """
        游戏名称
        """
        game: str

    def __init__(self, message_service):
        self.message_service = message_service
        super().__init__("stop_game", "根据游戏名停止服务器上的一个游戏服务器，要使用这个工具必须提到游戏名称",
                         self.StopGameParams)

    async def run(self, validated_params: StopGameParams):
        # 使用已校验和转换过的参数
        game = validated_params.game
        is_success = await self.message_service.stop_game(game)
        if is_success:
            return "停止游戏服务器成功"
        else:
            return "停止游戏服务器失败"


class CreateServerTool(BaseTool):
    def __init__(self, ali_client):
        self.ali_client = ali_client
        super().__init__("create_server", "创建阿里云服务器")

    async def run(self, validated_params):
        status = await self.ali_client.create_server()
        if status:
            return "创建服务器成功"
        else:
            return "创建服务器失败"


class StartServerTool(BaseTool):
    def __init__(self, ali_client):
        self.ali_client = ali_client
        super().__init__("start_server", "启动阿里云服务器")

    async def run(self, validated_params):
        server_status = await self.ali_client.start_server()
        if not server_status:
            return "启动服务器失败"
        return json.dumps(asdict(server_status))


class StopServerTool(BaseTool):
    def __init__(self, ali_client):
        self.ali_client = ali_client
        super().__init__("stop_server", "停止阿里云服务器")

    async def run(self, validated_params):
        status = await self.ali_client.stop_server()
        if status:
            return "停止服务器成功"
        else:
            return "停止服务器失败"


class ServerStatusTool(BaseTool):
    def __init__(self, ali_client):
        self.ali_client = ali_client
        super().__init__("server_status", "查看阿里云服务器信息")

    async def run(self, validated_params):
        status = await self.ali_client.get_server_status()
        if not status:
            return "获取服务器状态失败"
        else:
            return json.dumps(asdict(status))


class SearchEngineTool(BaseTool):
    class SearchEngineParams(BaseModel):
        """
        搜索关键词
        """
        keyword: str

    def __init__(self, search_client):
        self.search_client = search_client
        super().__init__("search_engine", "使用搜索引擎搜索关键词，搜索时建议使用中文", self.SearchEngineParams)

    async def run(self, validated_params: SearchEngineParams):
        keyword = validated_params.keyword
        result = await self.search_client.search(keyword)
        if not result:
            return "搜索失败"
        else:
            return result


class CleanHistoryTool(BaseTool):
    def __init__(self, history_cleaner):
        self.history_cleaner = history_cleaner
        super().__init__("clean_history", "清除聊天历史记录")

    async def run(self, validated_params):
        self.history_cleaner()
        return "历史记录已清空"
