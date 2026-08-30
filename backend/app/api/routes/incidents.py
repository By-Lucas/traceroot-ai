from fastapi import APIRouter
from sqlalchemy import select

from app.api.dependencies import CurrentUser, DbSession, owned_workspace
from app.core.config import get_settings
from app.models import Incident
from app.orchestration.engine import InvestigationEngine
from app.schemas.domain import IncidentCreate, IncidentResponse, InvestigationResponse
from app.services.domain import investigation_response, owned_incident

router = APIRouter(prefix="/incidents", tags=["incidents"])


@router.post("", response_model=IncidentResponse, status_code=201)
def create_incident(payload: IncidentCreate, user: CurrentUser, db: DbSession) -> Incident:
    workspace = owned_workspace(db, user)
    item = Incident(
        workspace_id=workspace.id,
        title=payload.title.strip(),
        description=payload.description.strip(),
        logs=payload.logs,
        stack_trace=payload.stack_trace,
        repository_path=payload.repository_path,
        git_url=str(payload.git_url) if payload.git_url else None,
        severity=payload.severity,
    )
    db.add(item)
    db.commit()
    db.refresh(item)
    return item


@router.get("", response_model=list[IncidentResponse])
def list_incidents(user: CurrentUser, db: DbSession) -> list[Incident]:
    workspace = owned_workspace(db, user)
    return list(
        db.scalars(
            select(Incident)
            .where(Incident.workspace_id == workspace.id)
            .order_by(Incident.created_at.desc())
        )
    )


@router.get("/{incident_id}", response_model=IncidentResponse)
def get_incident(incident_id: str, user: CurrentUser, db: DbSession) -> Incident:
    return owned_incident(db, incident_id, user)


@router.post("/{incident_id}/investigate", response_model=InvestigationResponse, status_code=201)
async def investigate(incident_id: str, user: CurrentUser, db: DbSession) -> InvestigationResponse:
    incident = owned_incident(db, incident_id, user)
    result = await InvestigationEngine(get_settings()).run(db, incident)
    return investigation_response(result)
