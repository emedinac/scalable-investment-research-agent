from datetime import UTC, datetime
from typing import Literal

from pydantic import BaseModel, Field


class Source(BaseModel):
    title: str
    url: str
    provider: str


class ValuationMetrics(BaseModel):
    current_price: float
    eps: float | None = None
    pe_ratio: float | None = None
    revenue_growth_yoy: float | None = None
    operating_margin: float | None = None
    valuation_label: Literal["attractive", "neutral", "expensive", "insufficient_data"]


class CacheMetadata(BaseModel):
    hit: bool
    key: str
    similarity: float | None = None


class TokenMetadata(BaseModel):
    model: str
    input_tokens: int
    output_tokens: int
    estimated_cost_usd: float


class ResearchResponse(BaseModel):
    query: str
    company: str
    ticker: str
    analysis: str
    valuation: ValuationMetrics
    risks: list[str]
    sources: list[Source]
    cache: CacheMetadata
    tokens: TokenMetadata
    created_at: datetime = Field(default_factory=lambda: datetime.now(UTC))


class QueryAcceptedResponse(BaseModel):
    task_id: str
    status: Literal["queued"]
