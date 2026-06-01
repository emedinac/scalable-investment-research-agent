import pytest
from httpx import ASGITransport, AsyncClient

from research_agent.main import main_app


@pytest.mark.asyncio
async def test_query_flow_with_mock_providers() -> None:
    transport = ASGITransport(app=main_app())
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        response = await client.get("/api/v1/query", params={"q": "Should I buy Google now?"})

    assert response.status_code == 200, response.text
    payload = response.json()
    assert payload["ticker"] == "GOOGL"
    assert payload["cache"]["hit"] is False
    assert "disclaimer" not in payload
    assert "you should buy" not in payload["analysis"].lower()


@pytest.mark.asyncio
async def test_metrics_endpoint() -> None:
    transport = ASGITransport(app=main_app())
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        response = await client.get("/metrics")

    assert response.status_code == 200, response.text
    assert "agent_requests_total" in response.text
