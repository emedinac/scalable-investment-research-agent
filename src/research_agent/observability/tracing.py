from research_agent.core.config import Settings


def configure_tracing(_settings: Settings) -> None:
    # Hook for OpenTelemetry/Langfuse trace initialization.
    return None
