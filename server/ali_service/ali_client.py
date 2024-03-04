import asyncio
import dataclasses
from typing import Literal, Optional

from ali_service.ali_sdk import AliSdk
from conf.config import CONFIG


@dataclasses.dataclass
class ServerStatus:
    status: Literal['Pending', 'Running', 'Stopped', 'Starting', 'Stopping']
    instance_id: str
    public_ip: Optional[str]


class AliClient:

    def __init__(self):
        self.sdk = AliSdk(
            access_key_id=CONFIG.aliyun.access_key_id,
            access_key_secret=CONFIG.aliyun.access_key_secret,
            region_id=CONFIG.aliyun.region_id
        )
        self.instance_name = CONFIG.aliyun.server_name
        self.disk_name = CONFIG.aliyun.disk_name
        self.template_name = CONFIG.aliyun.template_name

    async def get_server_status(self, instance_name=None) -> Optional[ServerStatus]:
        instance_name = instance_name or self.instance_name

        body = await self.sdk.get_server_status(instance_name)
        if not body:
            return None
        instance = body.instances.instance
        if len(instance) != 1:
            print("Instance not found or more than one instance found")
            return None
        instance = instance[0]
        instance_id = instance.instance_id
        print(f"Instance id {instance_id} status: {instance.status}")
        if instance.public_ip_address.ip_address:
            public_ip = instance.public_ip_address.ip_address[0]
            print(f"Public IP: {public_ip}")
        else:
            public_ip = None
        return ServerStatus(status=instance.status, public_ip=public_ip, instance_id=instance_id)

    async def create_instance(self):
        body = await self.sdk.describe_template(self.template_name)
        if not body or len(body.launch_template_sets.launch_template_set) != 1:
            return False
        template_id = body.launch_template_sets.launch_template_set[0].launch_template_id
        body = await self.sdk.run_instance(template_id)
        if not body or len(body.instance_id_sets.instance_id_set) != 1:
            return False
        return True

    async def start_server(self, instance_name=None) -> Optional[ServerStatus]:
        instance_name = instance_name or self.instance_name

        status = await self.get_server_status(self.instance_name)
        if not status:
            print("Server not found")
            return None
        instance_id = status.instance_id

        while True:
            disk_body = await self.sdk.describe_disk(self.disk_name)
            if not disk_body or len(disk_body.disks.disk) != 1:
                print("Disk not found or more than one disk found")
                return None

            disk = disk_body.disks.disk[0]

            if disk.status == 'In_use':
                if disk.instance_id != instance_id:
                    print(f"Disk is in use by another instance, detaching from that instance {disk.instance_id}")
                    await self.sdk.detach_disk(disk.instance_id, disk.disk_id)
                else:
                    print("Disk is in use by this instance")
                    break
            elif disk.status == 'Available':
                print(f"Disk is available, attaching to instance {instance_id}")
                await self.sdk.attach_disk(instance_id, disk.disk_id)
            elif disk.status in ['Attaching', 'Detaching', 'Creating', 'ReIniting']:
                print(f"Disk is {disk.status}")
            await asyncio.sleep(1)

        while True:
            status = await self.get_server_status(instance_name)
            if not status:
                print("Server not found")
                return None

            if status.status == 'Starting' or status.status == 'Pending':
                print("Server is starting or pending")
                await asyncio.sleep(1)
                continue
            elif status.status == 'Running':
                print(f"Server is running on IP: {status.public_ip}")
                return status
            elif status.status == 'Stopping':
                print("Server is stopping")
                await asyncio.sleep(3)
                continue
            elif status.status == 'Stopped':
                await self.sdk.start_instance(instance_id)
                await asyncio.sleep(3)
                continue

    async def stop_server(self, instance_name=None) -> bool:
        instance_name = instance_name or self.instance_name
        while True:
            status = await self.get_server_status(instance_name)
            if not status:
                print("Server not found")
                return False
            if status.status in ['Starting', 'Pending', 'Stopping']:
                print(f"Server is {status.status}")
                await asyncio.sleep(1)
                continue
            elif status.status == 'Stopped':
                print("Server is stopped")
                return True
            elif status.status == 'Running':
                print(f"Server is running on IP: {status.public_ip}")
                await self.sdk.stop_instance(status.instance_id)
                await asyncio.sleep(3)
                continue
