import json
import time
from pathlib import Path
from typing import Any

from sqlalchemy.orm import Session

from app.agents.contracts import InvestigationContext
from app.agents.evidence import collect_evidence
from app.agents.reproduction import reproduce
from app.agents.triage import run_triage
from app.agents.verification import verify
from app.core.config import Settings
from app.core.llm import create_provider
from app.models import AgentRun, Evidence, Hypothesis, Incident, Investigation, ToolCall, Trajectory


def _load_case_metadata(repository_path: str | None, allowed_base: Path) -> dict[str, Any]:
    if not repository_path:
        return {}
    case_file = Path(repository_path).resolve() / "case.json"
    try:
        case_file.relative_to(allowed_base.resolve())
    except ValueError:
        return {}
    if not case_file.is_file() or case_file.stat().st_size > 100_000:
        return {}
    return dict(json.loads(case_file.read_text(encoding="utf-8")))


class InvestigationEngine:
    def __init__(self, settings: Settings) -> None:
        self.settings = settings

    async def run(self, db: Session, incident: Incident) -> Investigation:
        started = time.perf_counter()
        investigation = Investigation(
            incident_id=incident.id, status="running", current_stage="triage"
        )
        db.add(investigation)
        db.flush()
        metadata = _load_case_metadata(incident.repository_path, self.settings.sandbox_root)
        context = InvestigationContext(
            title=incident.title,
            description=incident.description,
            logs=incident.logs,
            stack_trace=incident.stack_trace,
            repository_path=incident.repository_path,
            case_metadata=metadata,
        )
        provider = create_provider(self.settings)

        triage_started = time.perf_counter()
        triage = await run_triage(context, provider)
        triage_run = AgentRun(
            investigation_id=investigation.id,
            agent="triage",
            status="completed",
            summarized_decision=triage.summary,
            structured_output=triage.model_dump(),
            duration_ms=int((time.perf_counter() - triage_started) * 1000),
        )
        db.add(triage_run)
        for hyp in triage.hypotheses:
            db.add(
                Hypothesis(
                    investigation_id=investigation.id,
                    external_id=hyp.id,
                    claim=hyp.claim,
                    confidence=hyp.confidence,
                    reason=hyp.reason,
                    required_evidence=hyp.required_evidence,
                )
            )
        db.add(
            Trajectory(
                investigation_id=investigation.id,
                sequence=1,
                stage="triage",
                instruction_id="triage.v1",
                summarized_decision=triage.summary,
                input_summary={
                    "title": incident.title,
                    "artifact_lengths": {
                        "logs": len(incident.logs),
                        "stack": len(incident.stack_trace),
                    },
                },
                output=triage.model_dump(),
            )
        )

        investigation.current_stage = "evidence"
        evidence_started = time.perf_counter()
        evidence_items, sandbox = await collect_evidence(
            context, triage, provider, self.settings.sandbox_root
        )
        evidence_run = AgentRun(
            investigation_id=investigation.id,
            agent="evidence",
            status="completed",
            summarized_decision=f"Collected {len(evidence_items)} provenance-bound evidence items.",
            structured_output={"evidence": [item.model_dump() for item in evidence_items]},
            duration_ms=int((time.perf_counter() - evidence_started) * 1000),
        )
        db.add(evidence_run)
        db.flush()
        for item in evidence_items:
            db.add(
                Evidence(
                    investigation_id=investigation.id,
                    evidence_type=item.type,
                    location=item.location,
                    content_summary=item.content_summary,
                    supports=item.supports,
                    contradicts=item.contradicts,
                    confidence=item.confidence,
                    content_hash=item.content_hash,
                )
            )
        db.add(
            Trajectory(
                investigation_id=investigation.id,
                sequence=2,
                stage="evidence",
                instruction_id="evidence.v1",
                summarized_decision=evidence_run.summarized_decision,
                input_summary={"hypotheses": [item.id for item in triage.hypotheses]},
                output=evidence_run.structured_output,
            )
        )

        investigation.current_stage = "reproduction"
        repro = reproduce(sandbox)
        reproduction_run = AgentRun(
            investigation_id=investigation.id,
            agent="reproduction",
            status="completed" if repro.exit_code == 0 else "inconclusive",
            summarized_decision="Controlled reproduction matched H1."
            if repro.matched_hypotheses
            else "Controlled reproduction did not establish causality.",
            structured_output=repro.model_dump(),
            duration_ms=repro.duration_ms,
        )
        db.add(reproduction_run)
        db.flush()
        db.add(
            ToolCall(
                agent_run_id=reproduction_run.id,
                tool="execute_reproduction_script",
                arguments={"command_id": "reproduction"},
                response_summary=f"exit={repro.exit_code}; matched={repro.matched_hypotheses}",
                status="completed",
                duration_ms=repro.duration_ms,
            )
        )
        db.add(
            Trajectory(
                investigation_id=investigation.id,
                sequence=3,
                stage="reproduction",
                instruction_id="reproduction.v1",
                summarized_decision=reproduction_run.summarized_decision,
                input_summary={"command_id": "reproduction"},
                output=repro.model_dump(),
            )
        )

        investigation.current_stage = "verification"
        verification = verify(triage, evidence_items, repro)
        db.add(
            AgentRun(
                investigation_id=investigation.id,
                agent="verification",
                status="completed",
                summarized_decision=verification.rationale,
                structured_output=verification.model_dump(),
            )
        )
        db.add(
            Trajectory(
                investigation_id=investigation.id,
                sequence=4,
                stage="verification",
                instruction_id="verification.v1",
                summarized_decision=verification.rationale,
                input_summary={
                    "evidence_count": len(evidence_items),
                    "reproduction_exit": repro.exit_code,
                },
                output=verification.model_dump(),
                verification_feedback=verification.rationale,
            )
        )

        report = {
            "incident": {"title": incident.title, "severity": incident.severity},
            "status": verification.status,
            "executive_summary": triage.summary,
            "verified_root_cause": verification.root_cause,
            "confidence": verification.confidence,
            "timeline": [
                "Intake",
                "Triage",
                "Evidence",
                "Reproduction",
                "Verification",
                "Final Report",
            ],
            "hypotheses_considered": [item.model_dump() for item in triage.hypotheses],
            "evidence": [item.model_dump() for item in evidence_items],
            "reproduction": repro.model_dump(),
            "alternative_hypotheses_rejected": verification.rejected_alternatives,
            "recommended_fix": metadata.get(
                "recommended_fix", "Human review required before modifying production code."
            ),
            "regression_verification": verification.regression_status,
            "risk": "Deploying a fix without human approval may introduce a secondary regression.",
            "human_approval_requirement": "Required before production deployment.",
        }
        investigation.status = verification.status
        investigation.current_stage = "final_report"
        investigation.confidence = verification.confidence
        investigation.root_cause = verification.root_cause
        investigation.report = report
        investigation.duration_ms = int((time.perf_counter() - started) * 1000)
        incident.status = "investigated"
        db.commit()
        db.refresh(investigation)
        return investigation
