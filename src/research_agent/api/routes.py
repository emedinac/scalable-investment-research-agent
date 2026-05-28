from typing import Annotated

from fastapi import APIRouter, Depends, Query, Request
from prometheus_client import CONTENT_TYPE_LATEST, generate_latest
from starlette.responses import Response

from research_agent.agent.graph import ResearchGraph
from research_agent.api.dependencies import graph_dep
from research_agent.api.schemas import ResearchResponse
from research_agent.core.security import get_user_id
from research_agent.observability.metrics import REQUEST_LATENCY, REQUESTS
from research_agent.tasks.research import run_research_query

router = APIRouter()


@router.get("/health/live")
async def live() -> dict[str, str]:
    return {"status": "ok"}


@router.get("/health/ready")
async def ready(request: Request) -> dict[str, str]:
    graph_ready = hasattr(request.app.state, "graph")
    return {"status": "ready" if graph_ready else "starting"}


@router.get("/metrics")
async def metrics() -> Response:
    return Response(generate_latest(), media_type=CONTENT_TYPE_LATEST)


@router.get("/api/v1/query", response_model=ResearchResponse)
async def query(
    request: Request,
    q: Annotated[str, Query(min_length=3, max_length=500)],
    graph: Annotated[ResearchGraph, Depends(graph_dep)],
) -> ResearchResponse:
    user_id = get_user_id(request)
    with REQUEST_LATENCY.labels(endpoint="/api/v1/query").time():
        result = await graph.run(query=q, user_id=user_id)
    REQUESTS.labels(endpoint="/api/v1/query", cache_hit=str(result.cache.hit).lower()).inc()
    return result


@router.post("/api/v1/query/async")
async def query_async(
    request: Request,
    q: Annotated[str, Query(min_length=3, max_length=500)],
) -> dict[str, str]:
    task = run_research_query.delay(q, get_user_id(request))
    return {"task_id": task.id, "status": "queued"}
