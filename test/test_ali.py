import unittest

from ali_service.ali_client import AliClient
from conf.config import CONFIG


class MyTestCase(unittest.IsolatedAsyncioTestCase):
    async def test_get_server_status(self):
        client = AliClient()
        await client.get_server_status()

    async def test_start_server(self):
        client = AliClient()
        await client.start_server()

    async def test_stop_server(self):
        client = AliClient()
        await client.stop_server()


if __name__ == '__main__':
    unittest.main()
