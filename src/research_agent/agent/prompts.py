SYSTEM_PROMPT = (
    "You are an investment research analyst. Produce factual analysis only. "
    "Never provide personalized buy, sell, or hold recommendations."
)


def build_analysis_prompt(
    query: str,
    company: str,
    source_snippets: list[str],
    metrics: dict[str, object],
) -> str:
    context = "\n".join(source_snippets)
    return (
        f"{SYSTEM_PROMPT}\n"
        f"User query: {query}\n"
        f"Company: {company}\n"
        f"Metrics: {metrics}\n"
        f"Source context:\n{context}\n"
        "Return concise analysis with risks and no direct recommendation."
    )
