import json

from duckduckgo_search import AsyncDDGS

from search_service.search_client import SearchClient


class DuckDuckGoSearchClient(SearchClient):
    async def search(self, query: str) -> str:
        result = await AsyncDDGS(proxies=None).text(query, "zh-cn", max_results=10)
        return json.dumps(result, ensure_ascii=False)
