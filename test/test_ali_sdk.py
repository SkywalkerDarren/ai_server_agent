import unittest

from ali_service.ali_sdk import AliSdk
from conf.config import CONFIG


class MyTestCase(unittest.IsolatedAsyncioTestCase):

    async def asyncSetUp(self) -> None:
        self.client = AliSdk(
            access_key_id=CONFIG.aliyun.access_key_id,
            access_key_secret=CONFIG.aliyun.access_key_secret,
            region_id=CONFIG.aliyun.region_id,
            debug=True
        )

    async def test_get_server_status(self):
        body = await self.client.get_server_status(
            CONFIG.aliyun.server_name
        )
        if body.instances.instance:
            print(body.instances.instance[0].instance_id)
            print(body.instances.instance[0].instance_name)
            print(body.instances.instance[0].status)
            ip = body.instances.instance[0].public_ip_address.ip_address
            if ip:
                print(ip[0])

    async def test_start_instance(self):
        await self.client.start_instance(
            "i-wz90v25vmuglf1k2jwd1"
        )

    async def test_stop_instance(self):
        await self.client.stop_instance(
            "i-wz90v25vmuglf1k2jwd1"
        )

    async def test_describe_template(self):
        body = await self.client.describe_template(
            CONFIG.aliyun.template_name
        )
        print(body.launch_template_sets.launch_template_set[0].launch_template_id)

    async def test_run_instance(self):
        body = await self.client.run_instance(
            "lt-wz9b7tpk620eujyeha99"
        )
        print(body.instance_id_sets.instance_id_set[0])

    async def test_delete_instance(self):
        await self.client.delete_instance("i-wz921bxos35thbyymhd3")


    async def test_describe_disk(self):
        body = await self.client.describe_disk(
            CONFIG.aliyun.disk_name
        )
        print(body.disks.disk[0].status)
        print(body.disks.disk[0].disk_id)

    async def test_attach_disk(self):
        await self.client.attach_disk(
            "i-wz90v25vmuglf1k2jwd1",
            "d-wz9j9gotco5093bub0bp"
        )

    async def test_detach_disk(self):
        await self.client.detach_disk(
            "i-wz90v25vmuglf1k2jwd1",
            "d-wz9j9gotco5093bub0bp"
        )


if __name__ == '__main__':
    unittest.main()
