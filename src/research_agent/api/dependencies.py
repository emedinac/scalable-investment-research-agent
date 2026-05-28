from collections.abc import AsyncIterator

from fastapi import Request

from research_agent.agent.graph import ResearchGraph
from research_agent.cache.semantic_cache import SemanticCache
from research_agent.core.config import Settings, get_settings


def settings_dep() -> Settings:
    return get_settings()


async def graph_dep(request: Request) -> AsyncIterator[ResearchGraph]:
    yield request.app.state.graph


async def cache_dep(request: Request) -> AsyncIterator[SemanticCache]:
    yield request.app.state.cache
