from research_agent.providers.base import SearchProvider, SearchResult


async def fetch_research_sources(provider: SearchProvider, company: str) -> list[SearchResult]:
    return await provider.search(f"{company} latest earnings report guidance revenue margin")
