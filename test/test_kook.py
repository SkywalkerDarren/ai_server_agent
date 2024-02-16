import unittest

from kook_bot.kook_client import KookClient


class MyTestCase(unittest.IsolatedAsyncioTestCase):
    async def test_kook(self):
        client = KookClient()
        await client.start()

    async def test_kook_channel_list(self):
        client = KookClient()
        channel_list = await client.channel_list()
        print(channel_list)

    async def test_kook_guild_list(self):
        client = KookClient()
        guild_list = await client.guild_list()
        print(guild_list)


if __name__ == '__main__':
    unittest.main()
