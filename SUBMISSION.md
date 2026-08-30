# TraceRoot — Agentic Production Incident Investigator

## Description

TraceRoot turns production failures into evidence-backed incident reports. Instead of asking one assistant for a plausible diagnosis, it coordinates four bounded agents: Triage ranks hypotheses, Evidence records source/runtime provenance, Reproduction executes only allowlisted commands inside a sandbox, and Verification adversarially decides whether causality was actually established.

The product is a dark engineering command center built with Next.js and FastAPI. Engineers can register, create an incident, inspect a causal evidence graph, review exact source hashes and tool executions, replay observable trajectories, and open a structured final report. If the proof is incomplete, TraceRoot returns `UNVERIFIED`. It never hides failure and never deploys without human approval.

The repository includes PostgreSQL/SQLAlchemy/Alembic persistence, Argon2/JWT authentication, per-workspace authorization, OpenAI/Groq provider abstraction, a lightweight knowledge base, Prometheus-compatible metrics, Docker Compose, strict CI gates, ten reproducible incident repositories, a reasonable single-pass baseline and a deterministic VRCA evaluator.

In the executed offline demo evaluation, the baseline reached 90% raw accuracy but 0% Verified Root Cause Accuracy because it did not provide valid verification evidence. TraceRoot reproduced 10/10 curated cases and reached 100% deterministic VRCA with zero false-confident diagnoses. These results are explicitly scoped to the offline deterministic pipeline and are not presented as provider-backed LLM quality claims.

**Insight:** for incident investigation, better reasoning matters less than forcing the agent to prove itself.

## Run

Copy `.env.example` to `.env`, set a strong `SECRET_KEY`, then run `docker compose up --build`. Demo mode requires no LLM key. Open `http://localhost:3000`; API docs are at `http://localhost:8000/docs`.
