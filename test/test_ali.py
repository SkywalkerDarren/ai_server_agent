import unittest

from ali_service.ali_client import AliClient


class MyTestCase(unittest.IsolatedAsyncioTestCase):
    async def test_ali(self):
        client = AliClient()
        await client.get_server_status()

    async def test_start_instance(self):
        client = AliClient()
        await client.start_instance()

    async def test_stop_instance(self):
        client = AliClient()
        await client.stop_instance()

    async def test_reboot_instance(self):
        client = AliClient()
        await client.reboot_instance()

    async def test_start_server(self):
        client = AliClient()
        await client.start_server()

    async def test_stop_server(self):
        client = AliClient()
        await client.stop_server()

    async def test_run_command(self):
        client = AliClient()
        cmd = "ls"
        await client.execute_command(cmd)

    async def test_check_assistant_status(self):
        client = AliClient()
        await client.check_assistant_status()


if __name__ == '__main__':
    unittest.main()
