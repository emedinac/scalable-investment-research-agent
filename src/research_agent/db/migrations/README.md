Alembic migration scripts belong here.

The first production migration should create:

- `query_results`
- `token_usage`
- `price_snapshots`
- TimescaleDB hypertables for price and usage time series if enabled
