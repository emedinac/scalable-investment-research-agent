def route_model(query: str) -> str:
    lowered = query.lower()
    if "price" in lowered and "earnings" not in lowered and "buy" not in lowered:
        return "local-small"
    return "analysis-large"
