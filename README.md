# Scalable Investment Research Agent

Production-oriented Python scaffold for an investment research agent that returns
structured company analysis at scale without giving regulated buy/sell advice.

The service exposes `GET /api/v1/query?q=Should I buy Google now?`, resolves the
company/ticker, gathers market and earnings context, calculates simple valuation
signals, applies MiFID-aware guardrails, tracks token usage, caches similar
queries, and exports Prometheus metrics.

This is intentionally aproduction skeleton: external providers are behind
interfaces, and the app falls back to deterministic mock data when API keys are
missing so the whole stack can run locally.

## Quickstart

```bash
poetry install --with dev
poetry run uvicorn research_agent.main:main_app --factory --reload
```

Then open:

- API: <http://localhost:8000/api/v1/query?q=Should%20I%20buy%20Google%20now>
- Metrics: <http://localhost:8000/metrics>
- Health: <http://localhost:8000/health/ready>

To view API JSON in Streamlit, keep the API running and start the UI:

```bash
make ui
```

The Streamlit app lives at `streamlit_app.py` and is excluded from pytest
collection because tests are limited to the `tests/` directory.

Test with `curl`. The query endpoint uses `q` as a query parameter, so there is
no JSON request body:

```bash
curl -G "http://localhost:8000/api/v1/query" \
  --data-urlencode "q=Should I buy Google now?"

curl "http://localhost:8000/metrics"
curl "http://localhost:8000/health/ready"
```

The API response payload includes:

```json
{
  "query": "Should I buy Google now?",
  "company": "Alphabet Inc.",
  "ticker": "GOOGL",
  "analysis": "...",
  "valuation": {
    "current_price": 0.0,
    "eps": null,
    "pe_ratio": null,
    "revenue_growth_yoy": null,
    "operating_margin": null,
    "valuation_label": "insufficient_data"
  },
  "risks": ["..."],
  "sources": [
    {
      "title": "...",
      "url": "https://example.com",
      "provider": "..."
    }
  ],
  "disclaimer": "...",
  "cache": {
    "hit": false,
    "key": "...",
    "similarity": null
  },
  "tokens": {
    "model": "...",
    "input_tokens": 0,
    "output_tokens": 0,
    "estimated_cost_usd": 0.0
  },
  "created_at": "2026-05-27T00:00:00Z"
}
```

## Docker Compose

```bash
docker compose up --build
```

Services included:

- FastAPI API
- Celery worker
- PostgreSQL/TimescaleDB-compatible storage target
- Redis for cache, rate limiting, and Celery broker
- Prometheus and Grafana
- MinIO for DVC/eval artifact storage

## Production Intent

- Outputs are analysis only and must not include direct investment
  recommendations.
- Semantic cache and model routing are first-class cost controls.
- Every LLM call flows through token tracking.
- Prometheus/Grafana and Langfuse hooks are built in from day one.
- K8s manifests demonstrate API and worker scaling boundaries.

## Development

```bash
make install 
make run
make build
```

Other optiosn:

```bash
make test 
make clean
```
## Legal Note

This project is not financial advice software. It demonstrates engineering
architecture for research workflows. Any real deployment in Germany/EU requires
legal review under MiFID II and related regulations.
