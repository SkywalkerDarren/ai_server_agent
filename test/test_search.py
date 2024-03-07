import unittest

from search_service.search_client import SearchClient


class MyTestCase(unittest.IsolatedAsyncioTestCase):
    async def test_something(self):
        client = SearchClient()
        test = await client.search("今天的日期")
        print(test)


if __name__ == '__main__':
    unittest.main()
