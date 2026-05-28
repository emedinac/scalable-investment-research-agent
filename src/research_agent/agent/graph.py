from collections.abc import Callable
from typing import Any

from sqlalchemy.ext.asyncio import AsyncSession

from research_agent.agent.formatter import format_response
from research_agent.agent.prompts import build_analysis_prompt
from research_agent.api.schemas import CacheMetadata, ResearchResponse
from research_agent.cache.semantic_cache import SemanticCache
from research_agent.core.config import Settings
from research_agent.core.errors import GuardrailViolation
from research_agent.guardrails.input_policy import validate_input
from research_agent.guardrails.output_policy import validate_output
from research_agent.observability.metrics import CACHE_HIT_RATE, GUARDRAIL_BLOCKS
from research_agent.observability.token_tracker import TokenTracker
from research_agent.providers.base import LLMProvider, MarketDataProvider, SearchProvider
from research_agent.providers.llm import build_llm_provider
from research_agent.providers.mock_provider import MockMarketDataProvider, MockSearchProvider
from research_agent.providers.tavily import TavilySearchProvider
from research_agent.tools.financial_calculator import calculate_pe_ratio, valuation_label
from research_agent.tools.market_data import fetch_market_snapshot
from research_agent.tools.web_search import fetch_research_sources


class ResearchGraph:
    def __init__(
        self,
        cache: SemanticCache,
        search_provider: SearchProvider,
        market_provider: MarketDataProvider,
        llm_provider: LLMProvider,
        token_tracker: TokenTracker,
        db_session_factory: Callable[[], AsyncSession],
    ) -> None:
        self.cache = cache
        self.search_provider = search_provider
        self.market_provider = market_provider
        self.llm_provider = llm_provider
        self.token_tracker = token_tracker
        self.db_session_factory = db_session_factory

    async def run(self, query: str, user_id: str) -> ResearchResponse:
        try:
            validate_input(query)
        except GuardrailViolation:
            GUARDRAIL_BLOCKS.labels(policy="input").inc()
            raise

        lookup = await self.cache.get(query)
        CACHE_HIT_RATE.set(1 if lookup.hit else 0)
        if lookup.hit and lookup.value:
            response = lookup.value.model_copy(deep=True)
            response.cache = CacheMetadata(hit=True, key=lookup.key, similarity=lookup.similarity)
            return response

        market = await fetch_market_snapshot(self.market_provider, query)
        sources = await fetch_research_sources(self.search_provider, market.company)
        pe_ratio = calculate_pe_ratio(market)
        metrics: dict[str, Any] = {
            "current_price": market.current_price,
            "eps": market.eps,
            "pe_ratio": pe_ratio,
            "valuation_label": valuation_label(pe_ratio),
            "revenue_growth_yoy": market.revenue_growth_yoy,
            "operating_margin": market.operating_margin,
        }
        prompt = build_analysis_prompt(
            query=query,
            company=market.company,
            source_snippets=[source.snippet for source in sources],
            metrics=metrics,
        )
        llm_response = await self.llm_provider.synthesize(prompt)
        analysis = llm_response.text
        try:
            validate_output(analysis)
        except GuardrailViolation:
            GUARDRAIL_BLOCKS.labels(policy="output").inc()
            raise

        token_record = await self.token_tracker.track(
            user_id=user_id,
            model=llm_response.usage.model,
            input_tokens=llm_response.usage.input_tokens,
            output_tokens=llm_response.usage.output_tokens,
        )
        response = format_response(
            query=query,
            market=market,
            analysis=analysis,
            sources=sources,
            cache=CacheMetadata(hit=False, key=lookup.key),
            tokens=token_record,
        )
        await self.cache.set(query, response)
        return response


def build_research_graph(
    settings: Settings,
    cache: SemanticCache,
    db_session_factory: Callable[[], AsyncSession],
) -> ResearchGraph:
    search_provider: SearchProvider
    if settings.live_search_enabled and settings.tavily_api_key:
        search_provider = TavilySearchProvider(settings.tavily_api_key)
    else:
        search_provider = MockSearchProvider()

    return ResearchGraph(
        cache=cache,
        search_provider=search_provider,
        market_provider=MockMarketDataProvider(),
        llm_provider=build_llm_provider(settings.openai_api_key, settings.anthropic_api_key),
        token_tracker=TokenTracker(),
        db_session_factory=db_session_factory,
    )
