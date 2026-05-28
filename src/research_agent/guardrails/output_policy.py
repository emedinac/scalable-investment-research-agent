from research_agent.core.errors import GuardrailViolation

PROHIBITED_ADVICE = (
    "you should buy",
    "you should sell",
    "you must buy",
    "you must sell",
    "guaranteed return",
)


def validate_output(text: str) -> None:
    lowered = text.lower()
    for phrase in PROHIBITED_ADVICE:
        if phrase in lowered:
            raise GuardrailViolation(f"Output contains prohibited advice phrase: {phrase}")
