import json
import subprocess
import sys
import time
from pathlib import Path
from typing import Any

from fastapi import APIRouter, HTTPException

from app.api.dependencies import CurrentUser, DbSession, owned_workspace
from app.models import EvaluationRun

router = APIRouter(prefix="/evaluations", tags=["evaluations"])


@router.post("", status_code=202)
def start_evaluation(user: CurrentUser, db: DbSession) -> dict[str, Any]:
    workspace = owned_workspace(db, user)
    run = EvaluationRun(workspace_id=workspace.id, status="running")
    db.add(run)
    db.commit()
    started = time.perf_counter()
    root = Path(__file__).resolve().parents[4]
    result = subprocess.run(
        [sys.executable, "-m", "evals.run_eval"],
        cwd=root,
        capture_output=True,
        text=True,
        timeout=180,
        check=False,
    )
    run.duration_ms = int((time.perf_counter() - started) * 1000)
    if result.returncode == 0:
        run.status = "completed"
        run.results = json.loads((root / "results" / "comparison.json").read_text(encoding="utf-8"))
    else:
        run.status = "failed"
        run.results = {"error": result.stderr[-2000:]}
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
