.PHONY: install run ui test build clean

install:
	poetry install --with dev

run:
	poetry run uvicorn research_agent.main:main_app --factory --host 0.0.0.0 --port 8000 --reload

ui:
	poetry run streamlit run streamlit_app.py

test:
	poetry run pytest

build:
	docker compose build

clean:
	docker compose down --remove-orphans --volumes
	rm -rf .pytest_cache .ruff_cache htmlcov dist build *.egg-info
