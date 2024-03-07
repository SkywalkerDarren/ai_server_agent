import json
import os
from dataclasses import dataclass
from typing import Optional


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
class GoogleConfig:
    key: str
    cx: str
    cr: Optional[str]
    gl: Optional[str]
    num: Optional[int] = 10


@dataclass
class Config:
    openai: OpenAIConfig
    kook: KookConfig
    aliyun: AliyunConfig
    google: GoogleConfig

    @staticmethod
    def load() -> 'Config':
        with open(f"{os.path.dirname(__file__)}/../config.json") as f:
            config_data = json.load(f)
        return Config(
            openai=OpenAIConfig(**config_data.get('openai', {})),
            kook=KookConfig(**config_data.get('kook', {})),
            aliyun=AliyunConfig(**config_data.get('aliyun', {})),
            google=GoogleConfig(**config_data.get('google', {}))
        )


CONFIG = Config.load()
