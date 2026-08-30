# Improvement changelog

All reported measurements come from `python -m evals.run_eval` in deterministic offline demo mode. This mode measures pipeline behavior, not provider-backed LLM quality.

## Baseline — single-pass diagnosis

**What we tried:** one reasonable general-purpose diagnostic adapter received the incident, logs and source context with the instruction to determine root cause and recommend a fix.

**Result:** 90% raw root-cause accuracy, 0% VRCA, 10% false-confident diagnosis rate. It selected the misleading storage exception in case 10 and supplied neither reproduction nor verification evidence.

**Decision:** keep it as the comparison floor. High raw accuracy alone is insufficient for production incident work.

## Iteration 1 — structured evidence collection

**What we tried:** evidence items gained exact location, SHA-256 content hash, support/contradiction links and confidence.

**Why:** prose citations are hard to validate and easy to invent.

**Observed result:** all ten curated source markers were found and valid in the final offline run (100% evidence precision under the deterministic scorer).

**Decision:** retain first-class evidence entities and the frontend ledger.

## Iteration 2 — controlled reproduction loop

**What we tried:** each case received a minimal `reproduce.py`; execution moved behind a named allowlist and directory confinement.

**Why:** correlation in source and logs still does not prove the failure mechanism.

**Observed result:** 10/10 reproduction scripts exited zero with the expected marker. Traversal and arbitrary-command tests also passed.

**Decision:** reproduction is required for `VERIFIED` in the deterministic gate.

## Iteration 3 — independent verification agent

**What we tried:** a separate verifier evaluates source, runtime, reproduction and contradiction signals. Missing repository evidence returns `UNVERIFIED`; contradictory evidence can return `REJECTED`.

**Why:** the proposing agent should not grade its own diagnosis.

**Observed result:** TraceRoot VRCA reached 100% over the ten deterministic cases; the no-repository integration test correctly returned `UNVERIFIED`.

**Decision:** keep the verifier outside the triage/evidence agents and make its status the only report authority.

## Final

The largest measured offline change came from changing the acceptance criterion: a plausible claim no longer counted without provenance and reproduction. A provider-backed experiment is still required before claiming general improvement in reasoning capability.

No planning-agent experiment was implemented, so no removal claim is made.
