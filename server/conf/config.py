import json
import os


class Config:
    def __init__(self):
        with open(f"{os.path.dirname(__file__)}/../config.json") as f:
            data = json.load(f)
        self.kook_token = data['kook_token']
        self.openai_token = data['openai_token']
        self.kook_guild_id = data.get('kook_guild_id', '')
        self.kook_channel_id = data.get('kook_channel_id', '')
        self.kook_role_id = data.get('kook_role_id', '')
        self.kook_uid = data.get('kook_uid', '')


CONFIG = Config()
