import json

import aiohttp

from conf.config import CONFIG
from search_service.search_client import SearchClient


class GoogleSearchClient(SearchClient):

    def __init__(self):
        self.key = CONFIG.google.key
        self.cx = CONFIG.google.cx
        self.url = f"https://www.googleapis.com/customsearch/v1"
        self.cr = CONFIG.google.cr
        self.gl = CONFIG.google.gl
        self.num = CONFIG.google.num

    async def search(self, query: str) -> str:
        async with aiohttp.ClientSession() as session:
            async with session.get(
                    self.url,
                    params={
                        'key': self.key,
                        'cx': self.cx,
                        'q': query,
                        'cr': self.cr,
                        'gl': self.gl,
                        'num': self.num
                    }) as response:
                data = await response.json()
                items = self._filter_result(data['items'])
                return json.dumps(items, ensure_ascii=False)

    def _filter_result(self, results: list):
        return [
            {
                "title": item["title"],
                "link": item["link"],
                "snippet": item["snippet"]
            }
            for item in results
        ]
