import httpx

from research_agent.core.errors import ProviderError
from research_agent.providers.base import SearchResult


class TavilySearchProvider:
    def __init__(self, api_key: str) -> None:
        self.api_key = api_key

    async def search(self, query: str) -> list[SearchResult]:
        payload = {
            "api_key": self.api_key,
            "query": query,
            "search_depth": "advanced",
            "max_results": 5,
        }
        async with httpx.AsyncClient(timeout=20) as client:
            response = await client.post("https://api.tavily.com/search", json=payload)
        if response.is_error:
            raise ProviderError(f"Tavily search failed: {response.status_code}")
        data = response.json()
        return [
            SearchResult(
                title=item.get("title", "Untitled source"),
                url=item.get("url", ""),
                snippet=item.get("content", ""),
                provider="tavily",
            )
            for item in data.get("results", [])
        ]
