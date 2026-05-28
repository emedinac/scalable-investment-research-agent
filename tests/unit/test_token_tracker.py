import pytest

from research_agent.observability.token_tracker import TokenTracker


@pytest.mark.asyncio
async def test_token_tracker_records_mock_cost() -> None:
    record = await TokenTracker().track(
        user_id="user-1",
        model="mock-research-synthesizer",
        input_tokens=100,
        output_tokens=50,
    )

    assert record.estimated_cost_usd == 0.0
    assert record.input_tokens == 100
    assert record.output_tokens == 50
