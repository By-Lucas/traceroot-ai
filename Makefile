.PHONY: setup dev test lint eval migrate docker-build

setup:
	python -m venv .venv
	.venv/Scripts/python -m pip install -r backend/requirements-dev.txt
	cd frontend && npm install

dev:
	docker compose up --build

test:
	cd backend && ../.venv/Scripts/python -m pytest
	cd frontend && npm test

lint:
	.venv/Scripts/python -m ruff check backend
	.venv/Scripts/python -m ruff format --check backend
	cd backend && ../.venv/Scripts/python -m mypy app
	cd frontend && npm run lint && npm run type-check

eval:
	.venv/Scripts/python -m evals.run_eval

migrate:
	cd backend && ../.venv/Scripts/alembic upgrade head

docker-build:
	docker compose build
