import unittest

from conf.config import CONFIG
from kook_bot.kook_client import KookClient
from kook_bot.kook_websocket import KookWebsocket


class MyTestCase(unittest.IsolatedAsyncioTestCase):
    async def test_kook(self):
        client = KookWebsocket()
        await client.start()

    async def test_kook_channel_list(self):
        client = KookClient()
        channel_list = await client.channel_list(CONFIG.kook_guild_id)
        print(channel_list)

    async def test_kook_guild_list(self):
        client = KookClient()
        guild_list = await client.guild_list()
        print(guild_list)

    async def test_kook_guild_role_list(self):
        client = KookClient()
        guild_role_list = await client.guild_role_list(CONFIG.kook_guild_id)
        print(guild_role_list)

    async def test_kook_me(self):
        client = KookClient()
        me = await client.me()
        print(me)

    async def test_kook_user_view(self):
        client = KookClient()
        user_view = await client.user_view(CONFIG.kook_uid, CONFIG.kook_guild_id)
        print(user_view)


if __name__ == '__main__':
    unittest.main()
