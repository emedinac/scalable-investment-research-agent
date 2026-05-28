from typing import Any

import httpx
import streamlit as st

DEFAULT_API_BASE_URL = "http://localhost:8000"
DEFAULT_QUERY = "Should I buy Google now?"


def fetch_research_payload(api_base_url: str, query: str) -> dict[str, Any]:
    response = httpx.get(
        f"{api_base_url.rstrip('/')}/api/v1/query",
        params={"q": query},
        timeout=30,
    )
    response.raise_for_status()
    return response.json()


st.set_page_config(page_title="Investment Research JSON", layout="wide")

st.title("Investment Research JSON")

api_base_url = st.text_input("API base URL", value=DEFAULT_API_BASE_URL)
query = st.text_area("Query", value=DEFAULT_QUERY, height=100)

if st.button("Run query", type="primary"):
    if not query.strip():
        st.warning("Enter a query before running the request.")
    else:
        with st.spinner("Calling the research API..."):
            try:
                payload = fetch_research_payload(api_base_url, query.strip())
            except httpx.HTTPStatusError as exc:
                st.error(f"API returned {exc.response.status_code}")
                st.code(exc.response.text, language="json")
            except httpx.RequestError as exc:
                st.error(f"Could not reach the API: {exc}")
            else:
                st.success("Response received")
                st.json(payload, expanded=True)
