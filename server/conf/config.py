import json
import os


class Config:
    def __init__(self):
        with open(f"{os.path.dirname(__file__)}/../config.json") as f:
            data = json.load(f)
        self.openai_token = data['openai_token']
        self.kook_token = data['kook_token']
        self.kook_guild_id = data.get('kook_guild_id', '')
        self.kook_channel_id = data.get('kook_channel_id', '')
        self.kook_role_id = data.get('kook_role_id', '')
        self.kook_uid = data.get('kook_uid', '')
        self.aliyun_access_key_id = data['aliyun_access_key_id']
        self.aliyun_access_key_secret = data['aliyun_access_key_secret']
        self.aliyun_region_id = data['aliyun_region_id']
        self.aliyun_endpoint = data['aliyun_endpoint']
        self.aliyun_instance_id = data['aliyun_instance_id']


CONFIG = Config()
