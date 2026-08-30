from typing import Any

from fastapi import APIRouter
from sqlalchemy import select

from app.api.dependencies import CurrentUser, DbSession
from app.models import Trajectory
from app.schemas.domain import InvestigationResponse
from app.services.domain import investigation_response, owned_investigation

router = APIRouter(prefix="/investigations", tags=["investigations"])


@router.get("/{investigation_id}", response_model=InvestigationResponse)
def get_investigation(
    investigation_id: str, user: CurrentUser, db: DbSession
) -> InvestigationResponse:
    return investigation_response(owned_investigation(db, investigation_id, user))


@router.get("/{investigation_id}/trajectory")
def trajectory(investigation_id: str, user: CurrentUser, db: DbSession) -> list[dict[str, Any]]:
    owned_investigation(db, investigation_id, user)
    rows = db.scalars(
        select(Trajectory)
        .where(Trajectory.investigation_id == investigation_id)
        .order_by(Trajectory.sequence)
    )
    return [
        {
            "sequence": row.sequence,
            "stage": row.stage,
            "instruction_id": row.instruction_id,
            "summarized_decision": row.summarized_decision,
            "input": row.input_summary,
            "output": row.output,
            "verification_feedback": row.verification_feedback,
            "created_at": row.created_at,
        }
        for row in rows
    ]


@router.get("/{investigation_id}/report")
def report(investigation_id: str, user: CurrentUser, db: DbSession) -> dict[str, Any]:
    return owned_investigation(db, investigation_id, user).report
