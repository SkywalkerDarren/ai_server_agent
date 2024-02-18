import json
import os
from dataclasses import dataclass


@dataclass
class OpenAIConfig:
    token: str


@dataclass
class KookConfig:
    token: str
    guild_id: str
    channel_id: str
    role_id: str
    uid: str


@dataclass
class AliyunConfig:
    access_key_id: str
    access_key_secret: str
    region_id: str
    server_name: str
    template_name: str
    disk_name: str


@dataclass
class Config:
    openai: OpenAIConfig
    kook: KookConfig
    aliyun: AliyunConfig

    @staticmethod
    def load() -> 'Config':
        with open(f"{os.path.dirname(__file__)}/../config.json") as f:
            config_data = json.load(f)
        return Config(
            openai=OpenAIConfig(**config_data.get('openai', {})),
            kook=KookConfig(**config_data.get('kook', {})),
            aliyun=AliyunConfig(**config_data.get('aliyun', {}))
        )


CONFIG = Config.load()
