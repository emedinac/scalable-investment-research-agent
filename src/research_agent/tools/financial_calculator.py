from research_agent.providers.base import MarketSnapshot


def calculate_pe_ratio(snapshot: MarketSnapshot) -> float | None:
    if snapshot.eps in (None, 0):
        return None
    return round(snapshot.current_price / snapshot.eps, 2)


def valuation_label(pe_ratio: float | None) -> str:
    if pe_ratio is None:
        return "insufficient_data"
    if pe_ratio < 18:
        return "attractive"
    if pe_ratio <= 30:
        return "neutral"
    return "expensive"
