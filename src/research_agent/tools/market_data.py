from research_agent.providers.base import MarketDataProvider, MarketSnapshot


async def fetch_market_snapshot(provider: MarketDataProvider, query: str) -> MarketSnapshot:
    return await provider.snapshot(query)
