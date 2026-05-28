from typing import TypedDict

from research_agent.api.schemas import ResearchResponse
from research_agent.providers.base import MarketSnapshot, SearchResult


class ResearchState(TypedDict, total=False):
    query: str
    user_id: str
    company: str
    ticker: str
    sources: list[SearchResult]
    market: MarketSnapshot
    analysis: str
    response: ResearchResponse
