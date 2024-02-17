import asyncio
import base64
import dataclasses
import json
import os
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
        self.runtime = util_models.RuntimeOptions(
            autoretry=True,
            ignore_ssl=True
        )

    @property
    def client(self):
        config = open_api_models.Config(
            access_key_id=CONFIG.aliyun_access_key_id,
            access_key_secret=CONFIG.aliyun_access_key_secret
        )
        config.endpoint = CONFIG.aliyun_endpoint

        return Ecs20140526Client(config)

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
            if instance:
                print(f"Instance {CONFIG.aliyun_instance_id} status: {instance.status}")
                if instance.public_ip_address.ip_address:
                    public_ip = instance.public_ip_address.ip_address[0]
                    print(f"Public IP: {public_ip}")
                else:
                    public_ip = None
                return ServerStatus(status=instance.status, public_ip=public_ip)
            else:
                print("Instance not found")
                return None

        except Exception as error:
            print(f"get_server_status error: {error}")
            return None

    async def run_command(self, command: str) -> Optional[str]:
        run_command_request = ecs_20140526_models.RunCommandRequest(
            region_id=CONFIG.aliyun_region_id,
            type='RunShellScript',
            command_content=command,
            working_dir='/',
            instance_id=[
                CONFIG.aliyun_instance_id,
            ],
            username='root',
            timeout=60
        )
        try:
            # 复制代码运行请自行打印 API 的返回值
            resp = await self.client.run_command_with_options_async(run_command_request, self.runtime)
            return resp.body.invoke_id
        except Exception as error:
            print(f"run_command error: {error}")

    async def query_command_result(self, command_id: str):
        describe_invocation_results_request = ecs_20140526_models.DescribeInvocationResultsRequest(
            region_id=CONFIG.aliyun_region_id,
            invoke_id=command_id
        )
        try:
            # 复制代码运行请自行打印 API 的返回值
            resp = await self.client.describe_invocation_results_with_options_async(describe_invocation_results_request,
                                                                                    self.runtime)
            invoke = resp.body.invocation.invocation_results.invocation_result[0]
            print(resp.body.invocation)
            return invoke
        except Exception as error:
            print(f"query_command_result error: {error}")

    async def check_assistant_status(self):
        describe_cloud_assistant_status_request = ecs_20140526_models.DescribeCloudAssistantStatusRequest(
            region_id=CONFIG.aliyun_region_id,
            ostype='Linux',
            instance_id=[
                CONFIG.aliyun_instance_id
            ]
        )
        try:
            resp = await self.client.describe_cloud_assistant_status_with_options_async(
                describe_cloud_assistant_status_request, self.runtime)
            status = resp.body.instance_cloud_assistant_status_set.instance_cloud_assistant_status[
                0].cloud_assistant_status
            return status == 'true'
        except Exception as error:
            print(f"check_assistant_status error: {error}")

    async def execute_command(self, command: str):
        invoke_id = await self.run_command(command)
        while True:
            invoke = await self.query_command_result(invoke_id)
            if not invoke:
                print("Command not found")
                return
            if invoke.invoke_record_status == 'Running':
                await asyncio.sleep(1)
                continue
            elif invoke.invoke_record_status == 'Finished':
                output = base64.b64decode(invoke.output).decode('utf-8')
                print(f"Command finished with output:\n{output}")
                return
            elif invoke.invoke_record_status == 'Failed':
                exit_code = invoke.exit_code
                print(f"Command failed with exit code: {exit_code}")
                return
            elif invoke.invoke_record_status == 'Stopped':
                print("Command stopped")
                return
            elif invoke.invoke_record_status == 'Stopping':
                print("Command stopping")
                await asyncio.sleep(1)
                continue


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
                while not await self.check_assistant_status():
                    await asyncio.sleep(1)
                with open(f"{os.path.dirname(__file__)}/startup.sh", 'r', encoding='utf-8') as f:
                    command = f.read()
                await self.execute_command(command)
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
