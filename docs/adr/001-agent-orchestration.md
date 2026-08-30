# ADR 001: Explicit bounded orchestration

Status: Accepted

Use an explicit Python state machine for the linear four-agent workflow. The orchestrator owns stage order, persistence and budgets. Agents cannot recursively invoke one another. This is easier to audit and test than introducing a graph framework for a fixed sequence.
