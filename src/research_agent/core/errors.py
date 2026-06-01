class ResearchAgentError(Exception):
    """Base exception for expected application failures."""


class GuardrailViolation(ResearchAgentError):
    """Raised when input or output violates compliance policy."""


class ProviderError(ResearchAgentError):
    """Raised when an external provider fails."""
