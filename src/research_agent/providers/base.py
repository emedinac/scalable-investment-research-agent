from dataclasses import dataclass
from typing import Protocol


@dataclass(frozen=True)
class SearchResult:
    title: str
    url: str
    snippet: str
    provider: str


@dataclass(frozen=True)
class MarketSnapshot:
    ticker: str
    current_price: float
    eps: float | None
    revenue_growth_yoy: float | None
    operating_margin: float | None


@dataclass(frozen=True)
class LLMUsage:
    model: str
    input_tokens: int
    output_tokens: int


@dataclass(frozen=True)
class LLMResponse:
    text: str
    usage: LLMUsage


class SearchProvider(Protocol):
    async def search(self, query: str) -> list[SearchResult]:
        raise NotImplementedError


class MarketDataProvider(Protocol):
    async def snapshot(self, company_or_ticker: str) -> MarketSnapshot:
        raise NotImplementedError


class LLMProvider(Protocol):
    async def synthesize(self, prompt: str) -> LLMResponse:
        raise NotImplementedError
