from prometheus_client import Counter, Gauge, Histogram

REQUESTS = Counter(
    "agent_requests_total",
    "Total API requests.",
    labelnames=("endpoint", "cache_hit"),
)
REQUEST_LATENCY = Histogram(
    "agent_latency_seconds",
    "Agent request latency.",
    labelnames=("endpoint",),
)
TOKEN_USAGE = Counter(
    "token_usage_total",
    "Total tracked LLM tokens.",
    labelnames=("model", "direction"),
)
LLM_COST = Counter(
    "llm_cost_usd_total",
    "Estimated LLM cost in USD.",
    labelnames=("model",),
)
CACHE_HIT_RATE = Gauge("cache_hit_rate", "Last observed cache hit status as 1 or 0.")
GUARDRAIL_BLOCKS = Counter(
    "guardrail_blocks_total",
    "Total guardrail blocks.",
    labelnames=("policy",),
)
