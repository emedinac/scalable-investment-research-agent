from celery import Celery

from research_agent.core.config import get_settings

settings = get_settings()

celery_app = Celery(
    "research_agent",
    broker=settings.celery_broker_url,
    backend=settings.celery_result_backend,
    include=["research_agent.tasks.research"],
)
celery_app.conf.update(
    task_track_started=True,
    worker_prefetch_multiplier=1,
    task_acks_late=True,
)


def worker_main() -> None:
    celery_app.worker_main()
