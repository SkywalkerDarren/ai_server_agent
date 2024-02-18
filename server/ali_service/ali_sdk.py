import json
import traceback
from typing import Optional, Any

from alibabacloud_ecs20140526.client import Client as Ecs20140526Client
from alibabacloud_tea_openapi import models as open_api_models
from alibabacloud_ecs20140526 import models as ecs_20140526_models
from alibabacloud_tea_util import models as util_models


class AliSdk:

    def __init__(self, access_key_id, access_key_secret, region_id, debug=False):
        self.debug = debug
        self.runtime = util_models.RuntimeOptions(
            autoretry=True,
            ignore_ssl=True
        )
        config = open_api_models.Config(
            access_key_id=access_key_id,
            access_key_secret=access_key_secret,
            region_id=region_id,
        )
        self.region_id = region_id
        self.client = Ecs20140526Client(config)

    def _on_response(self, resp):
        if self.debug:
            print(resp.body)

    def _on_error(self, error):
        if self.debug:
            print(f"error: {error}")
            traceback.print_exc()

    async def get_server_status(self, instance_name: str) -> Optional[Any]:
        describe_instances_request = ecs_20140526_models.DescribeInstancesRequest(
            region_id=self.region_id,
            instance_name=instance_name
        )
        try:
            resp = await self.client.describe_instances_with_options_async(describe_instances_request,
                                                                           self.runtime)
            self._on_response(resp)
            return resp.body
        except Exception as error:
            self._on_error(error)
            return None

    async def start_instance(self, instance_id: str) -> Optional[Any]:
        start_instance_request = ecs_20140526_models.StartInstanceRequest(
            instance_id=instance_id
        )
        try:
            resp = await self.client.start_instance_with_options_async(start_instance_request, self.runtime)
            self._on_response(resp)
            return resp.body
        except Exception as error:
            self._on_error(error)
            return None

    async def describe_template(self, template_name: str) -> Optional[Any]:
        describe_launch_templates_request = ecs_20140526_models.DescribeLaunchTemplatesRequest(
            region_id=self.region_id,
            launch_template_name=[
                template_name
            ]
        )
        try:
            resp = await self.client.describe_launch_templates_with_options_async(describe_launch_templates_request, self.runtime)
            self._on_response(resp)
            return resp.body
        except Exception as error:
            self._on_error(error)
            return None
    async def stop_instance(self, instance_id: str) -> Optional[Any]:
        stop_instance_request = ecs_20140526_models.StopInstanceRequest(
            force_stop=True,
            instance_id=instance_id,
            stopped_mode='StopCharging'
        )
        try:
            resp = await self.client.stop_instance_with_options_async(stop_instance_request, self.runtime)
            self._on_response(resp)
            return resp.body
        except Exception as error:
            self._on_error(error)
            return None

    async def run_instance(self, template_id) -> Optional[Any]:
        run_instances_request = ecs_20140526_models.RunInstancesRequest(
            region_id=self.region_id,
            launch_template_id=template_id
        )
        try:
            resp = await self.client.run_instances_with_options_async(run_instances_request, self.runtime)
            self._on_response(resp)
            return resp.body
        except Exception as error:
            self._on_error(error)
            return None

    async def delete_instance(self, instance_id: str) -> Optional[Any]:
        delete_instance_request = ecs_20140526_models.DeleteInstanceRequest(
            instance_id=instance_id,
            force=True
        )
        try:
            resp = await self.client.delete_instance_with_options_async(delete_instance_request, self.runtime)
            self._on_response(resp)
            return resp.body
        except Exception as error:
            self._on_error(error)
            return None

    async def describe_disk(self, disk_name: str) -> Optional[Any]:
        describe_disks_request = ecs_20140526_models.DescribeDisksRequest(
            region_id=self.region_id,
            disk_name=disk_name
        )
        try:
            resp = await self.client.describe_disks_with_options_async(describe_disks_request, self.runtime)
            self._on_response(resp)
            return resp.body
        except Exception as error:
            self._on_error(error)
            return None

    async def attach_disk(self, instance_id: str, disk_id: str) -> Optional[Any]:
        attach_disk_request = ecs_20140526_models.AttachDiskRequest(
            delete_with_instance=False,
            bootable=False,
            instance_id=instance_id,
            disk_id=disk_id
        )
        try:
            resp = await self.client.attach_disk_with_options_async(attach_disk_request, self.runtime)
            self._on_response(resp)
            return resp.body
        except Exception as error:
            self._on_error(error)
            return None

    async def detach_disk(self, instance_id: str, disk_id: str):
        detach_disk_request = ecs_20140526_models.DetachDiskRequest(
            instance_id=instance_id,
            disk_id=disk_id
        )
        try:
            resp = await self.client.detach_disk_with_options_async(detach_disk_request, self.runtime)
            self._on_response(resp)
            return resp.body
        except Exception as error:
            self._on_error(error)
            return None
