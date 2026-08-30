import json
import time
from pathlib import Path
from typing import Any

from fastapi import APIRouter, HTTPException

from app.api.dependencies import CurrentUser, DbSession, owned_workspace
from app.core.config import get_settings
from app.models import EvaluationRun
from app.tools.sandbox import RepositorySandbox

router = APIRouter(prefix="/evaluations", tags=["evaluations"])


def _run_case(case_dir: Path, sandbox_root: Path) -> dict[str, Any]:
    metadata = json.loads((case_dir / "case.json").read_text(encoding="utf-8"))
    evidence_file = str(metadata.get("evidence_file", "app.py"))
    marker = str(metadata.get("evidence_marker", ""))
    sandbox = RepositorySandbox(case_dir, sandbox_root)
    source = sandbox.read_file(evidence_file)
    reproduction = sandbox.run("reproduction")
    evidence_found = bool(marker and marker in source)
    reproduced = reproduction.exit_code == 0 and "TRACEROOT_REPRODUCED" in reproduction.stdout
    return {
        "slug": metadata["slug"],
        "title": metadata["title"],
        "status": "VERIFIED" if evidence_found and reproduced else "UNVERIFIED",
        "evidence_found": evidence_found,
        "reproduced": reproduced,
        "duration_ms": reproduction.duration_ms,
        "command": reproduction.command,
    }


@router.post("", status_code=202)
def start_evaluation(user: CurrentUser, db: DbSession) -> dict[str, Any]:
    workspace = owned_workspace(db, user)
    run = EvaluationRun(workspace_id=workspace.id, status="running")
    db.add(run)
    db.commit()
    started = time.perf_counter()
    root = get_settings().sandbox_root.resolve()
    try:
        cases = [_run_case(path.parent, root) for path in sorted(root.glob("*/case.json"))]
        verified = sum(case["status"] == "VERIFIED" for case in cases)
        reproduced = sum(bool(case["reproduced"]) for case in cases)
        evidence = sum(bool(case["evidence_found"]) for case in cases)
        total = len(cases)
        run.status = "completed"
        run.results = {
            "mode": "executed_sandbox_cases",
            "metrics": {
                "cases": total,
                "verified_rate": verified / total if total else 0,
                "reproduction_success_rate": reproduced / total if total else 0,
                "evidence_precision": evidence / total if total else 0,
            },
            "cases": cases,
        }
    except (OSError, ValueError, KeyError, json.JSONDecodeError) as error:
        run.status = "failed"
        run.results = {"error": str(error)}
    run.duration_ms = int((time.perf_counter() - started) * 1000)
    db.commit()
    return {"id": run.id, "status": run.status}


@router.get("/{evaluation_id}")
def get_evaluation(evaluation_id: str, user: CurrentUser, db: DbSession) -> dict[str, Any]:
    workspace = owned_workspace(db, user)
    run = db.get(EvaluationRun, evaluation_id)
    if not run or run.workspace_id != workspace.id:
        raise HTTPException(status_code=404, detail="Evaluation not found")
    return {
        "id": run.id,
        "status": run.status,
        "results": run.results,
        "duration_ms": run.duration_ms,
    }
