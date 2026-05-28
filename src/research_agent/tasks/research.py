import asyncio

from research_agent.agent.graph import build_research_graph
from research_agent.cache.semantic_cache import SemanticCache
from research_agent.core.config import get_settings
from research_agent.db.session import create_session_factory
from research_agent.tasks.celery_app import celery_app


@celery_app.task(name="research_agent.tasks.run_research_query")
def run_research_query(query: str, user_id: str = "anonymous") -> dict:
    return asyncio.run(_run(query=query, user_id=user_id))


async def _run(query: str, user_id: str) -> dict:
    settings = get_settings()
    graph = build_research_graph(
        settings=settings,
        cache=SemanticCache(settings),
        db_session_factory=create_session_factory(settings.database_url),
    )
    response = await graph.run(query=query, user_id=user_id)
    return response.model_dump(mode="json")
