from typing import Literal, cast

from research_agent.api.schemas import (
    CacheMetadata,
    ResearchResponse,
    Source,
    TokenMetadata,
    ValuationMetrics,
)
from research_agent.observability.token_tracker import TokenRecord
from research_agent.providers.base import MarketSnapshot, SearchResult
from research_agent.tools.financial_calculator import calculate_pe_ratio, valuation_label


def format_response(
    query: str,
    market: MarketSnapshot,
    analysis: str,
    sources: list[SearchResult],
    cache: CacheMetadata,
    tokens: TokenRecord,
) -> ResearchResponse:
    pe_ratio = calculate_pe_ratio(market)
    return ResearchResponse(
        query=query,
        company=market.company,
        ticker=market.ticker,
        analysis=analysis,
        valuation=ValuationMetrics(
            current_price=market.current_price,
            eps=market.eps,
            pe_ratio=pe_ratio,
            revenue_growth_yoy=market.revenue_growth_yoy,
            operating_margin=market.operating_margin,
            valuation_label=cast(
                Literal["attractive", "neutral", "expensive", "insufficient_data"],
                valuation_label(pe_ratio),
            ),
        ),
        risks=[
            "Market prices can change faster than cached analysis.",
            "Financial metrics may be incomplete or provider-dependent.",
            "Macroeconomic, regulatory, and execution risks can affect outcomes.",
        ],
        sources=[Source(title=s.title, url=s.url, provider=s.provider) for s in sources],
        cache=cache,
        tokens=TokenMetadata(
            model=tokens.model,
            input_tokens=tokens.input_tokens,
            output_tokens=tokens.output_tokens,
            estimated_cost_usd=tokens.estimated_cost_usd,
        ),
    )
