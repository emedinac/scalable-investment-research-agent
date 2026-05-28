from dataclasses import dataclass

from research_agent.observability.metrics import LLM_COST, TOKEN_USAGE
from research_agent.providers.llm import estimate_cost_usd


@dataclass(frozen=True)
class TokenRecord:
    user_id: str
    model: str
    input_tokens: int
    output_tokens: int
    estimated_cost_usd: float


class TokenTracker:
    async def track(
        self,
        user_id: str,
        model: str,
        input_tokens: int,
        output_tokens: int,
    ) -> TokenRecord:
        cost = estimate_cost_usd(model, input_tokens, output_tokens)
        TOKEN_USAGE.labels(model=model, direction="input").inc(input_tokens)
        TOKEN_USAGE.labels(model=model, direction="output").inc(output_tokens)
        LLM_COST.labels(model=model).inc(cost)
        return TokenRecord(
            user_id=user_id,
            model=model,
            input_tokens=input_tokens,
            output_tokens=output_tokens,
            estimated_cost_usd=cost,
        )
