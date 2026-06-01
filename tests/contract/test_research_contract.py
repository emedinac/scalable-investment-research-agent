import pytest
from httpx import ASGITransport, AsyncClient

from research_agent.main import main_app


@pytest.mark.asyncio
async def test_response_contract_avoids_direct_advice() -> None:
    transport = ASGITransport(app=main_app())
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        response = await client.get("/api/v1/query", params={"q": "Should I buy Google now?"})

    assert response.status_code == 200, response.text
    payload = response.json()

    combined_text = payload["analysis"].lower()

    assert "disclaimer" not in payload
    assert "you should buy" not in combined_text
    assert "you should sell" not in combined_text
    assert payload["risks"]
    assert payload["sources"]
