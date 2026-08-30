# Reproduction guide

This guide assumes a clean machine.

## Requirements

- Git
- Docker Desktop / Engine with Compose v2
- For native development: Python 3.12, Node.js 22+, npm 10+

## Docker path

```bash
git clone <repository-url> traceroot
cd traceroot
cp .env.example .env
# Set SECRET_KEY to a long random value in .env.
docker compose up --build
```

Wait for PostgreSQL health and Alembic migration, then open `http://localhost:3000`. Register, create an incident and use an approved path such as `/evaluation_cases/02_null_handling_regression` inside the backend container.

## Native path

```bash
make setup
cp .env.example .env
cd backend
../.venv/Scripts/alembic upgrade head  # Windows
../.venv/Scripts/uvicorn app.main:app --reload
```

In a second terminal:

```bash
cd frontend
npm run dev
```

On POSIX, replace `.venv/Scripts` with `.venv/bin` in Makefile commands if needed.

## Exact validation commands

```bash
make lint
make test
make eval
docker build -t traceroot-backend backend
docker build -t traceroot-frontend frontend
```

Evaluation writes:

- `results/baseline.json`
- `results/traceroot.json`
- `results/comparison.json`
- `results/comparison.md`
- representative files under `trajectories/`

The offline suite takes approximately one second on a modern laptop and costs $0 because it makes no provider calls. Provider-backed runtime and cost depend on the selected model and are not estimated here without an actual run.

## Provider-backed mode

Set exactly one provider key and configure:

```dotenv
LLM_PROVIDER=openai
LLM_MODEL=<supported-model>
OPENAI_API_KEY=<secret>
```

or `LLM_PROVIDER=groq` with `GROQ_API_KEY`. Never commit `.env`.

## Expected golden path

1. Register and receive JWTs.
2. Create a null-regression incident with its runtime log and case repository.
3. Run investigation.
4. Observe four persisted agent runs and trajectory stages.
5. Confirm source and runtime provenance.
6. Confirm allowlisted reproduction exits zero with `TRACEROOT_REPRODUCED`.
7. Open a `VERIFIED` report with 96% deterministic confidence and required human approval.
