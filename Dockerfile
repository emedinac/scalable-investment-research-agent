FROM python:3.12-slim AS base

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    POETRY_VERSION=2.1.4 \
    POETRY_NO_INTERACTION=1 \
    POETRY_VIRTUALENVS_CREATE=false

WORKDIR /app

RUN pip install --no-cache-dir "poetry==$POETRY_VERSION"

COPY pyproject.toml README.md ./
RUN poetry install --only main --no-root

COPY src ./src
RUN poetry install --only main

EXPOSE 8000

CMD ["uvicorn", "research_agent.main:main_app", "--factory", "--host", "0.0.0.0", "--port", "8000"]
