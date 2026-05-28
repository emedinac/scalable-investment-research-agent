def passes_guardrail_contract(answer: str) -> bool:
    lowered = answer.lower()
    return "not a recommendation" in lowered and "you should buy" not in lowered
