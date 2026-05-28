import pytest

from research_agent.cache.semantic_cache import SemanticCache
from research_agent.core.config import Settings


@pytest.mark.asyncio
async def test_semantic_cache_exact_hit() -> None:
    cache = SemanticCache(Settings(semantic_cache_threshold=0.92))
    await cache.set("Should I buy Google now?", {"answer": "cached"})

    lookup = await cache.get("Should I buy Google now?")

    assert lookup.hit is True
    assert lookup.value == {"answer": "cached"}
    assert lookup.similarity == 1.0


@pytest.mark.asyncio
async def test_semantic_cache_miss() -> None:
    cache = SemanticCache(Settings(semantic_cache_threshold=0.99))
    await cache.set("Should I buy Google now?", {"answer": "cached"})

    lookup = await cache.get("What is Microsoft revenue growth?")

    assert lookup.hit is False
