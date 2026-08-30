# Five-minute demo script

## 0:00–0:30 — problem

Show the dashboard. “During an incident, logs, source, configuration and tests tell different fragments of the story. A generic assistant can give a plausible diagnosis quickly. TraceRoot asks a harder question: can it prove it?”

## 0:30–1:00 — baseline

Open Evaluations. Explain that the single-pass baseline receives the same incident, logs and source. It scores 90% raw accuracy offline, but zero VRCA because it does not collect valid evidence or reproduce the cause. Call out misleading case 10 and the 10% false-confidence rate.

## 1:00–2:45 — TraceRoot execution

Create the null-handling incident. Paste the runtime error and select the synthetic repository. Start investigation. On the command center, walk through Triage, Evidence, Reproduction and Verification. Show H1/H2, source hash, support edge, reproduction terminal and `VERIFIED` gate. Stress that no raw LLM shell command executes.

## 2:45–3:30 — measured results

Return to Evaluations. TraceRoot reproduced 10/10 offline cases and achieved 100% deterministic VRCA. State the caveat on-screen: this validates orchestration and scoring, not provider-backed LLM quality. No fabricated benchmark claim.

## 3:30–4:10 — improvement changelog

Show the changelog: baseline, provenance, reproduction, independent verifier. Connect each iteration to a measured behavior.

## 4:10–4:35 — removed experiment

Say: “We considered a separate planning agent but did not implement or claim a removed experiment. The workflow is linear, so explicit orchestration stayed clearer and cheaper.”

## 4:35–5:00 — hot take

End on the final report. “For incident investigation, better reasoning mattered less than forcing the agent to prove itself. TraceRoot does not deploy. It gives the engineer a causal, reviewable record and asks for human approval.”
