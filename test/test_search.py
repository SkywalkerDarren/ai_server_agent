import unittest

from search_service.duckduckgo_search import DuckDuckGoSearchClient
from search_service.google_search import GoogleSearchClient
from search_service.search_client import SearchClient
from search_service.search_service import SearchService


class MyTestCase(unittest.IsolatedAsyncioTestCase):
    async def test_google_search(self):
        client = GoogleSearchClient()
        test = await client.search("今天的日期")
        print(test)

    async def test_ddgs_search(self):
        client = DuckDuckGoSearchClient()
        test = await client.search("今天的日期")
        print(test)

    async def test_search(self):
        client = SearchService()
        test = await client.search("今天的日期")
        print(test)


if __name__ == '__main__':
    unittest.main()
