from research_agent.providers.base import MarketSnapshot
from research_agent.tools.financial_calculator import calculate_pe_ratio, valuation_label


def test_calculate_pe_ratio() -> None:
    snapshot = MarketSnapshot(
        ticker="GOOGL",
        current_price=174.25,
        eps=7.42,
        revenue_growth_yoy=0.14,
        operating_margin=0.31,
    )

    assert calculate_pe_ratio(snapshot) == 23.48
    assert valuation_label(23.48) == "neutral"


def test_valuation_label_without_eps() -> None:
    assert valuation_label(None) == "insufficient_data"
