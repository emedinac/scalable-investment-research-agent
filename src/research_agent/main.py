import uvicorn
from fastapi import FastAPI
from fastapi.responses import JSONResponse

from research_agent.agent.graph import build_research_graph
from research_agent.api.routes import router
from research_agent.cache.semantic_cache import SemanticCache
from research_agent.core.config import get_settings
from research_agent.core.errors import GuardrailViolation
from research_agent.core.logging import configure_logging
from research_agent.db.session import create_session_factory
from research_agent.observability.tracing import configure_tracing


def main_app() -> FastAPI:
    settings = get_settings()
    configure_logging(settings.log_level)
    configure_tracing(settings)

    app = FastAPI(title=settings.app_name, version="0.1.0")
    app.state.db_session_factory = create_session_factory(settings.database_url)
    app.state.cache = SemanticCache(settings=settings)
    app.state.graph = build_research_graph(
        settings=settings,
        cache=app.state.cache,
        db_session_factory=app.state.db_session_factory,
    )

    @app.exception_handler(GuardrailViolation)
    async def guardrail_handler(_request, exc: GuardrailViolation) -> JSONResponse:
        return JSONResponse(status_code=422, content={"detail": str(exc)})

    app.include_router(router)
    return app


def run() -> None:
    settings = get_settings()
    uvicorn.run(
        "research_agent.main:main_app",
        factory=True,
        host=settings.api_host,
        port=settings.api_port,
    )
