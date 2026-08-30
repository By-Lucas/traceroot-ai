from typing import Any

from fastapi import HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session, selectinload

from app.models import Incident, Investigation, User
from app.schemas.domain import InvestigationResponse


def owned_incident(db: Session, incident_id: str, user: User) -> Incident:
    incident = db.scalar(
        select(Incident).where(Incident.id == incident_id, Incident.workspace.has(owner_id=user.id))
    )
    if not incident:
        raise HTTPException(status_code=404, detail="Incident not found")
    return incident


def owned_investigation(db: Session, investigation_id: str, user: User) -> Investigation:
    item = db.scalar(
        select(Investigation)
        .options(selectinload(Investigation.hypotheses), selectinload(Investigation.evidence))
        .where(
            Investigation.id == investigation_id,
            Investigation.incident.has(Incident.workspace.has(owner_id=user.id)),
        )
    )
    if not item:
        raise HTTPException(status_code=404, detail="Investigation not found")
    return item


def investigation_response(item: Investigation) -> InvestigationResponse:
    hypotheses: list[dict[str, Any]] = [
        {
            "id": h.external_id,
            "claim": h.claim,
            "confidence": h.confidence,
            "reason": h.reason,
            "required_evidence": h.required_evidence,
            "disposition": h.disposition,
        }
        for h in item.hypotheses
    ]
    evidence: list[dict[str, Any]] = [
        {
            "id": e.id,
            "type": e.evidence_type,
            "location": e.location,
            "content_summary": e.content_summary,
            "supports": e.supports,
            "contradicts": e.contradicts,
            "confidence": e.confidence,
            "content_hash": e.content_hash,
        }
        for e in item.evidence
    ]
    return InvestigationResponse(
        id=item.id,
        incident_id=item.incident_id,
        status=item.status,
        current_stage=item.current_stage,
        confidence=item.confidence,
        root_cause=item.root_cause,
        report=item.report,
        duration_ms=item.duration_ms,
        token_usage=item.token_usage,
        approximate_cost_usd=item.approximate_cost_usd,
        hypotheses=hypotheses,
        evidence=evidence,
    )
