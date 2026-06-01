from research_agent.core.errors import GuardrailViolation

BLOCKED_PATTERNS = (
    "guarantee profit",
    "risk-free",
    "insider",
    "leverage all",
    "certain profit",
)


def validate_input(query: str) -> None:
    lowered = query.lower()
    for pattern in BLOCKED_PATTERNS:
        if pattern in lowered:
            raise GuardrailViolation(f"Blocked unsafe investment request pattern: {pattern}")
