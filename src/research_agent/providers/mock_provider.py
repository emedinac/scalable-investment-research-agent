from research_agent.providers.base import LLMResponse, LLMUsage, MarketSnapshot, SearchResult

COMPANY_ALIASES = {
    "google": ("Alphabet Inc.", "GOOGL"),
    "alphabet": ("Alphabet Inc.", "GOOGL"),
    "meta": ("Meta Platforms Inc.", "META"),
    "facebook": ("Meta Platforms Inc.", "META"),
    "amazon": ("Amazon.com Inc.", "AMZN"),
    "apple": ("Apple Inc.", "AAPL"),
    "microsoft": ("Microsoft Corp.", "MSFT"),
    "tesla": ("Tesla Inc.", "TSLA"),
}


class MockSearchProvider:
    async def search(self, query: str) -> list[SearchResult]:
        return [
            SearchResult(
                title="Latest quarterly earnings release",
                url="https://example.com/earnings/latest",
                snippet=(
                    f"Mock earnings context for {query}: revenue growth, margin trend, "
                    "and guidance."
                ),
                provider="mock",
            ),
            SearchResult(
                title="Recent market news summary",
                url="https://example.com/news/latest",
                snippet=(
                    "Mock news context: advertising demand and cloud profitability "
                    "are key watch items."
                ),
                provider="mock",
            ),
        ]


class MockMarketDataProvider:
    async def snapshot(self, company_or_ticker: str) -> MarketSnapshot:
        lowered = company_or_ticker.lower()
        company, ticker = next(
            (value for key, value in COMPANY_ALIASES.items() if key in lowered),
            ("Alphabet Inc.", "GOOGL"),
        )
        return MarketSnapshot(
            company=company,
            ticker=ticker,
            current_price=174.25,
            eps=7.42,
            revenue_growth_yoy=0.14,
            operating_margin=0.31,
        )


class MockLLMProvider:
    async def synthesize(self, prompt: str) -> LLMResponse:
        input_tokens = max(1, len(prompt.split()))
        text = (
            "The company shows resilient fundamentals based on the available earnings context, "
            "with positive revenue growth and strong operating margin. Valuation should be "
            "interpreted alongside concentration risk, macro sensitivity, and execution risk. "
            "This analysis does not instruct the user to buy, sell, or hold the security."
        )
        return LLMResponse(
            text=text,
            usage=LLMUsage(
                model="mock-research-synthesizer",
                input_tokens=input_tokens,
                output_tokens=48,
            ),
        )
