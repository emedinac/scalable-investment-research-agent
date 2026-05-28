from sqlalchemy.ext.asyncio import AsyncSession

from research_agent.api.schemas import ResearchResponse
from research_agent.db.models import QueryResult, TokenUsage
from research_agent.observability.token_tracker import TokenRecord


async def save_query_result(
    session: AsyncSession,
    user_id: str,
    response: ResearchResponse,
) -> None:
    session.add(
        QueryResult(
            user_id=user_id,
            query=response.query,
            company=response.company,
            ticker=response.ticker,
            response=response.model_dump(mode="json"),
        )
    )
    await session.commit()


async def save_token_usage(session: AsyncSession, record: TokenRecord) -> None:
    session.add(
        TokenUsage(
            user_id=record.user_id,
            model=record.model,
            input_tokens=record.input_tokens,
            output_tokens=record.output_tokens,
            cost_usd=record.estimated_cost_usd,
        )
    )
    await session.commit()
