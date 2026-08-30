from fastapi import APIRouter, HTTPException
from sqlalchemy import select
from sqlalchemy.orm import selectinload

from app.api.dependencies import CurrentUser, DbSession, owned_workspace
from app.knowledge.service import chunk_document, content_hash, terms
from app.models import KnowledgeChunk, KnowledgeDocument
from app.schemas.domain import KnowledgeCreate, KnowledgeResponse

router = APIRouter(prefix="/knowledge", tags=["knowledge"])


@router.post("", response_model=KnowledgeResponse, status_code=201)
def ingest(payload: KnowledgeCreate, user: CurrentUser, db: DbSession) -> KnowledgeResponse:
    workspace = owned_workspace(db, user)
    digest = content_hash(payload.content)
    duplicate = db.scalar(
        select(KnowledgeDocument).where(
            KnowledgeDocument.workspace_id == workspace.id, KnowledgeDocument.content_hash == digest
        )
    )
    if duplicate:
        raise HTTPException(status_code=409, detail="This document was already ingested")
    doc = KnowledgeDocument(
        workspace_id=workspace.id,
        title=payload.title,
        source_type=payload.source_type,
        source_name=payload.source_name,
        content_hash=digest,
    )
    db.add(doc)
    db.flush()
    pieces = chunk_document(payload.content)
    for index, chunk in enumerate(pieces):
        db.add(
            KnowledgeChunk(
                document_id=doc.id, chunk_index=index, content=chunk, search_terms=terms(chunk)
            )
        )
    db.commit()
    db.refresh(doc)
    return KnowledgeResponse(
        id=doc.id,
        title=doc.title,
        source_type=doc.source_type,
        source_name=doc.source_name,
        chunk_count=len(pieces),
        created_at=doc.created_at,
    )


@router.get("", response_model=list[KnowledgeResponse])
def list_documents(user: CurrentUser, db: DbSession) -> list[KnowledgeResponse]:
    workspace = owned_workspace(db, user)
    docs = db.scalars(
        select(KnowledgeDocument)
        .options(selectinload(KnowledgeDocument.chunks))
        .where(KnowledgeDocument.workspace_id == workspace.id)
        .order_by(KnowledgeDocument.created_at.desc())
    )
    return [
        KnowledgeResponse(
            id=d.id,
            title=d.title,
            source_type=d.source_type,
            source_name=d.source_name,
            chunk_count=len(d.chunks),
            created_at=d.created_at,
        )
        for d in docs
    ]
