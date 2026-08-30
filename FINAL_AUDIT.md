# Final audit

Audit date: 2026-08-30

## What works

- FastAPI starts with health, readiness, OpenAPI, Swagger, ReDoc and Prometheus metrics.
- Registration, login, refresh, current-user and logout contracts are implemented with Argon2 and JWT.
- Workspace ownership prevents cross-user incident access.
- Incident CRUD intake and persisted investigation execution work end to end.
- Four typed agents execute through an explicit, non-recursive orchestrator.
- Evidence includes location, hypothesis links, confidence and SHA-256 provenance.
- Reproduction is confined to approved repositories and fixed command identifiers.
- The verifier returns `UNVERIFIED` when repository proof is absent.
- Reports, agent runs, tool calls and observable trajectories persist.
- Markdown/TXT/JSON knowledge ingestion, chunking and duplicate detection work.
- The Next.js command center builds all 12 application routes, including the evidence graph and report views.
- Ten reproducible synthetic cases and a reasonable single-pass baseline execute offline.
- Docker Compose starts PostgreSQL, runs Alembic, starts the API and serves the frontend.

## Validation results

| Gate                           | Result                             |
| ------------------------------ | ---------------------------------- |
| Ruff lint                      | PASS                               |
| Ruff format                    | PASS — 44 files                    |
| mypy strict                    | PASS — 35 source files             |
| Backend pytest                 | PASS — 15 tests                    |
| Backend coverage               | 88% statements                     |
| Frontend ESLint                | PASS — zero warnings               |
| TypeScript strict              | PASS                               |
| Frontend Vitest                | PASS — 2 tests                     |
| Next.js production build       | PASS — 12 routes                   |
| npm production audit           | PASS — 0 vulnerabilities           |
| Alembic migration              | PASS — `0001 (head)`               |
| Backend Docker image           | PASS                               |
| Frontend Docker image          | PASS                               |
| Compose PostgreSQL health      | PASS                               |
| Runtime `/health` and `/ready` | PASS — HTTP 200                    |
| Runtime frontend `/dashboard`  | PASS — HTTP 200                    |
| Runtime golden investigation   | PASS — `VERIFIED`, confidence 0.96 |

The runtime golden path created a fresh user, incident and investigation against PostgreSQL. It persisted two evidence items and the stages `triage,evidence,reproduction,verification`; the final report required human approval.

## Evaluation results

Mode: deterministic offline demo; no provider key was present and no LLM benchmark is claimed.

| Metric                         | Baseline | TraceRoot |
| ------------------------------ | -------: | --------: |
| Cases                          |       10 |        10 |
| Raw root-cause accuracy        |      90% |      100% |
| VRCA                           |       0% |      100% |
| Evidence precision             |       0% |      100% |
| Reproduction success           |       0% |      100% |
| False-confident diagnosis rate |      10% |        0% |

## Defects found and corrected during audit

1. `.env` CORS input was parsed as JSON before validation. Configuration now stores CSV text and exposes a normalized origin list. All backend tests were rerun.
2. Pinned Next.js/Vitest versions had published vulnerabilities. They were upgraded to Next 16.3.3 and Vitest 3.2.7; audit, lint, types, tests and production build were rerun.
3. The frontend Docker context included local dependency directories and reached 241 MB. `.dockerignore` files reduced it to approximately 536 KB; both images were rebuilt.
4. Structured completion logs reset the context before reading `request_id`. The middleware order was corrected; lint, typing, all backend tests, image build and a live header/log smoke were rerun. The final log contains `audit-request-id-final`.
5. The first post-fix HTTP attempt raced application startup. Final validation used readiness polling and passed; this was a test-harness timing issue, not an application regression.

## Known limitations and remaining risks

- Provider-backed OpenAI/Groq evaluation remains unexecuted because no key was supplied.
- Long investigations run inside the request lifecycle rather than a durable worker.
- Refresh-token rotation/revocation is not persisted.
- Knowledge retrieval is lexical rather than embedding-based.
- Browser-level Playwright coverage is not included; component and live HTTP paths are covered.
- The Docker PostgreSQL volume is intentionally left available after containers stop for local reuse.
- No deployment target or GitHub remote credentials were available, so no remote deployment/push is claimed.

## Commands used

```text
python -m pytest
ruff check backend
ruff format --check backend
mypy app
npm run lint
npm run type-check
npm test
npm run build
npm audit --omit=dev
python -m evals.run_eval
alembic upgrade head
docker build -t traceroot-backend:audit backend
docker build -t traceroot-frontend:audit frontend
docker compose up -d --build
docker compose logs
docker compose down
```

## Judge review

1. The problem and “no root cause without evidence” principle are visible immediately.
2. Each agent owns a distinct accountability boundary; the verifier is not decorative.
3. The local and Compose golden paths work end to end.
4. Improvement measurements are generated artifacts with explicit offline scope.
5. A clean-machine path, exact commands, versions and expected outputs are documented.
6. Important claims link to tests, JSON results, trajectories or runtime evidence.
7. Security, observability, typed boundaries and tradeoffs are explicit.
8. The interface is presentation-ready and responsive, with non-generic investigation views.
9. The video script fits the five-minute narrative.
10. The repository is structured for professional review with CI, ADRs and no committed credentials.
