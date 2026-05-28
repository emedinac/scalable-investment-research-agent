from research_agent.providers.base import LLMProvider
from research_agent.providers.mock_provider import MockLLMProvider


def build_llm_provider(openai_api_key: str | None, anthropic_api_key: str | None) -> LLMProvider:
    # The provider boundary is intentionally real, but the first version uses a
    # deterministic fallback so local demos never depend on paid API keys.
    _ = (openai_api_key, anthropic_api_key)
    return MockLLMProvider()


def estimate_cost_usd(model: str, input_tokens: int, output_tokens: int) -> float:
    if model.startswith("mock"):
        return 0.0
    token_price_per_1k = 0.003
    return round(((input_tokens + output_tokens) / 1000) * token_price_per_1k, 6)
