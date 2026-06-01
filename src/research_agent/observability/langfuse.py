from research_agent.core.config import Settings


def langfuse_enabled(settings: Settings) -> bool:
    return bool(settings.langfuse_public_key and settings.langfuse_secret_key)
