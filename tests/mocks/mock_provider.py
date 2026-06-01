from research_agent.providers.base import (
    LLMResponse,
    LLMUsage,
    MarketSnapshot,
    SearchResult,
)


class MockSearchProvider:
    async def search(self, query: str) -> list[SearchResult]:
        _ = query
        return [
            SearchResult(
                title="Alphabet Q1 earnings overview",
                url="https://example.com/alphabet-q1",
                snippet="Alphabet reported steady search growth, expanding cloud revenue, and disciplined expenses.",
                provider="mock",
            ),
            SearchResult(
                title="Analyst view on Alphabet margins",
                url="https://example.com/alphabet-margins",
                snippet="Analysts highlighted durable operating margins and ongoing AI infrastructure investment.",
                provider="mock",
            ),
        ]


class MockMarketDataProvider:
    async def snapshot(self, company_or_ticker: str) -> MarketSnapshot:
        _ = company_or_ticker
        snapshot = MarketSnapshot(
            ticker="GOOGL",
            current_price=174.25,
            eps=7.42,
            revenue_growth_yoy=0.14,
            operating_margin=0.31,
        )
        object.__setattr__(snapshot, "company", "Alphabet Inc.")
        return snapshot


class MockLLMProvider:
    async def synthesize(self, prompt: str) -> LLMResponse:
        return LLMResponse(
            text=(
                "Alphabet looks financially solid based on the provided metrics, "
                "with a neutral valuation profile, healthy margins, and continued "
                "revenue growth. Investors can compare the valuation with their "
                "own objectives and risk tolerance."
            ),
            usage=LLMUsage(
                model="mock-research-synthesizer",
                input_tokens=max(1, len(prompt.split())),
                output_tokens=42,
            ),
        )
