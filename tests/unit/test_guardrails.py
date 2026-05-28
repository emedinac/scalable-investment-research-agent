import pytest

from research_agent.core.errors import GuardrailViolation
from research_agent.guardrails.input_policy import validate_input
from research_agent.guardrails.output_policy import validate_output


def test_blocks_unsafe_input() -> None:
    with pytest.raises(GuardrailViolation):
        validate_input("Give me a risk-free guaranteed profit trade")


def test_blocks_direct_advice_output() -> None:
    with pytest.raises(GuardrailViolation):
        validate_output("You should buy this stock today.")


def test_allows_research_language() -> None:
    validate_output("This is analysis only and not a recommendation to buy or sell.")
