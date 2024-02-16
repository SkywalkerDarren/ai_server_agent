import asyncio
import dataclasses
import json
from typing import Literal, Optional

from conf.config import CONFIG
from alibabacloud_ecs20140526.client import Client as Ecs20140526Client
from alibabacloud_tea_openapi import models as open_api_models
from alibabacloud_ecs20140526 import models as ecs_20140526_models
from alibabacloud_tea_util import models as util_models


@dataclasses.dataclass
class ServerStatus:
    status: Literal['Pending', 'Running', 'Stopped', 'Starting', 'Stopping']
    public_ip: Optional[str]


class AliClient:
    def __init__(self):
        config = open_api_models.Config(
            access_key_id=CONFIG.aliyun_access_key_id,
            access_key_secret=CONFIG.aliyun_access_key_secret
        )
        config.endpoint = CONFIG.aliyun_endpoint
        self.runtime = util_models.RuntimeOptions(
            autoretry=True,
            ignore_ssl=True
        )
        self.client = Ecs20140526Client(config)

    async def start_instance(self):
        start_instance_request = ecs_20140526_models.StartInstanceRequest(
            instance_id=CONFIG.aliyun_instance_id
        )
        try:
            resp = await self.client.start_instance_with_options_async(start_instance_request, self.runtime)
            print(resp.body)
        except Exception as error:
            print(f"start_instance error: {error}")

    async def stop_instance(self):
        stop_instance_request = ecs_20140526_models.StopInstanceRequest(
            force_stop=True,
            instance_id=CONFIG.aliyun_instance_id,
            stopped_mode='StopCharging'
        )
        try:
            resp = await self.client.stop_instance_with_options_async(stop_instance_request, self.runtime)
            print(resp.body)
        except Exception as error:
            print(f"stop_instance error: {error}")

    async def reboot_instance(self):
        reboot_instance_request = ecs_20140526_models.RebootInstanceRequest(
            force_stop=True,
            instance_id=CONFIG.aliyun_instance_id
        )
        try:
            resp = await self.client.reboot_instance_with_options_async(reboot_instance_request, self.runtime)
            print(resp.body)
        except Exception as error:
            print(f"reboot_instance error: {error}")

    async def get_server_status(self) -> Optional[ServerStatus]:
        describe_instances_request = ecs_20140526_models.DescribeInstancesRequest(
            region_id=CONFIG.aliyun_region_id,
            instance_ids=json.dumps([CONFIG.aliyun_instance_id])
        )
        try:
            resp = await self.client.describe_instances_with_options_async(describe_instances_request,
                                                                           self.runtime)
            instance = resp.body.instances.instance[0]
            print(instance)
            if instance:
                print(f"Instance {CONFIG.aliyun_instance_id} status: {instance.status}")
                if instance.public_ip_address.ip_address:
                    public_ip = instance.public_ip_address.ip_address[0]
                    print(f"Public IP: {public_ip}")
                else:
                    public_ip = None
                return ServerStatus(status=instance.status, public_ip=public_ip)
            else:
                return None

        except Exception as error:
            print(f"get_server_status error: {error}")
            return None

    async def start_server(self) -> Optional[ServerStatus]:
        while True:
            status = await self.get_server_status()
            if not status:
                print("Server not found")
                return None
            if status.status == 'Starting' or status.status == 'Pending':
                print("Server is starting or pending")
                await asyncio.sleep(1)
                continue
            if status.status == 'Running':
                print(f"Server is running on IP: {status.public_ip}")
                await asyncio.sleep(1)
                return status
            if status.status == 'Stopping':
                print("Server is stopping")
                await asyncio.sleep(3)
                continue
            if status.status == 'Stopped':
                await self.start_instance()
                await asyncio.sleep(3)
                continue

    async def stop_server(self) -> bool:
        while True:
            status = await self.get_server_status()
            if not status:
                print("Server not found")
                return False
            if status.status == 'Starting' or status.status == 'Pending':
                print("Server is starting or pending")
                await asyncio.sleep(1)
                continue
            if status.status == 'Stopping':
                print("Server is stopping or pending")
                await asyncio.sleep(1)
                continue
            if status.status == 'Stopped':
                print("Server is stopped")
                return True
            if status.status == 'Running':
                print(f"Server is running on IP: {status.public_ip}")
                await self.stop_instance()
                await asyncio.sleep(3)
                continue
