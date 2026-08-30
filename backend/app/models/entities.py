import uuid
from datetime import UTC, datetime
from typing import Any

from sqlalchemy import JSON, Boolean, DateTime, Float, ForeignKey, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base


def uuid_str() -> str:
    return str(uuid.uuid4())


class TimestampMixin:
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=lambda: datetime.now(UTC)
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(UTC),
        onupdate=lambda: datetime.now(UTC),
    )


class User(Base, TimestampMixin):
    __tablename__ = "users"
    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=uuid_str)
    email: Mapped[str] = mapped_column(String(320), unique=True, index=True)
    password_hash: Mapped[str] = mapped_column(String(255))
    display_name: Mapped[str] = mapped_column(String(120))
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    workspaces: Mapped[list["Workspace"]] = relationship(
        back_populates="owner", cascade="all, delete-orphan"
    )


class Workspace(Base, TimestampMixin):
    __tablename__ = "workspaces"
    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=uuid_str)
    name: Mapped[str] = mapped_column(String(120))
    owner_id: Mapped[str] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"), index=True)
    owner: Mapped[User] = relationship(back_populates="workspaces")
    incidents: Mapped[list["Incident"]] = relationship(
        back_populates="workspace", cascade="all, delete-orphan"
    )


class Incident(Base, TimestampMixin):
    __tablename__ = "incidents"
    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=uuid_str)
    workspace_id: Mapped[str] = mapped_column(
        ForeignKey("workspaces.id", ondelete="CASCADE"), index=True
    )
    title: Mapped[str] = mapped_column(String(240))
    description: Mapped[str] = mapped_column(Text)
    logs: Mapped[str] = mapped_column(Text, default="")
    stack_trace: Mapped[str] = mapped_column(Text, default="")
    repository_path: Mapped[str | None] = mapped_column(String(500), nullable=True)
    git_url: Mapped[str | None] = mapped_column(String(500), nullable=True)
    severity: Mapped[str] = mapped_column(String(20), default="high")
    status: Mapped[str] = mapped_column(String(30), default="open")
    workspace: Mapped[Workspace] = relationship(back_populates="incidents")
    investigations: Mapped[list["Investigation"]] = relationship(
        back_populates="incident", cascade="all, delete-orphan"
    )


class Investigation(Base, TimestampMixin):
    __tablename__ = "investigations"
    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=uuid_str)
    incident_id: Mapped[str] = mapped_column(
        ForeignKey("incidents.id", ondelete="CASCADE"), index=True
    )
    status: Mapped[str] = mapped_column(String(40), default="intake")
    current_stage: Mapped[str] = mapped_column(String(40), default="intake")
    confidence: Mapped[float] = mapped_column(Float, default=0.0)
    root_cause: Mapped[str | None] = mapped_column(Text, nullable=True)
    report: Mapped[dict[str, Any]] = mapped_column(JSON, default=dict)
    duration_ms: Mapped[int] = mapped_column(Integer, default=0)
    token_usage: Mapped[int] = mapped_column(Integer, default=0)
    approximate_cost_usd: Mapped[float] = mapped_column(Float, default=0.0)
    incident: Mapped[Incident] = relationship(back_populates="investigations")
    hypotheses: Mapped[list["Hypothesis"]] = relationship(cascade="all, delete-orphan")
    evidence: Mapped[list["Evidence"]] = relationship(cascade="all, delete-orphan")
    agent_runs: Mapped[list["AgentRun"]] = relationship(cascade="all, delete-orphan")
    trajectories: Mapped[list["Trajectory"]] = relationship(cascade="all, delete-orphan")


class Hypothesis(Base, TimestampMixin):
    __tablename__ = "hypotheses"
    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=uuid_str)
    investigation_id: Mapped[str] = mapped_column(
        ForeignKey("investigations.id", ondelete="CASCADE"), index=True
    )
    external_id: Mapped[str] = mapped_column(String(20))
    claim: Mapped[str] = mapped_column(Text)
    confidence: Mapped[float] = mapped_column(Float)
    reason: Mapped[str] = mapped_column(Text)
    required_evidence: Mapped[list[str]] = mapped_column(JSON, default=list)
    disposition: Mapped[str] = mapped_column(String(30), default="pending")


class Evidence(Base, TimestampMixin):
    __tablename__ = "evidence"
    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=uuid_str)
    investigation_id: Mapped[str] = mapped_column(
        ForeignKey("investigations.id", ondelete="CASCADE"), index=True
    )
    evidence_type: Mapped[str] = mapped_column(String(50))
    location: Mapped[str] = mapped_column(String(500))
    content_summary: Mapped[str] = mapped_column(Text)
    supports: Mapped[list[str]] = mapped_column(JSON, default=list)
    contradicts: Mapped[list[str]] = mapped_column(JSON, default=list)
    confidence: Mapped[float] = mapped_column(Float)
    content_hash: Mapped[str] = mapped_column(String(64))


class AgentRun(Base, TimestampMixin):
    __tablename__ = "agent_runs"
    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=uuid_str)
    investigation_id: Mapped[str] = mapped_column(
        ForeignKey("investigations.id", ondelete="CASCADE"), index=True
    )
    agent: Mapped[str] = mapped_column(String(40))
    status: Mapped[str] = mapped_column(String(30))
    summarized_decision: Mapped[str] = mapped_column(Text)
    structured_output: Mapped[dict[str, Any]] = mapped_column(JSON, default=dict)
    duration_ms: Mapped[int] = mapped_column(Integer, default=0)
    token_usage: Mapped[int] = mapped_column(Integer, default=0)
    tool_calls: Mapped[list["ToolCall"]] = relationship(cascade="all, delete-orphan")


class ToolCall(Base, TimestampMixin):
    __tablename__ = "tool_calls"
    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=uuid_str)
    agent_run_id: Mapped[str] = mapped_column(
        ForeignKey("agent_runs.id", ondelete="CASCADE"), index=True
    )
    tool: Mapped[str] = mapped_column(String(80))
    arguments: Mapped[dict[str, Any]] = mapped_column(JSON, default=dict)
    response_summary: Mapped[str] = mapped_column(Text)
    status: Mapped[str] = mapped_column(String(30))
    duration_ms: Mapped[int] = mapped_column(Integer, default=0)


class Trajectory(Base, TimestampMixin):
    __tablename__ = "trajectories"
    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=uuid_str)
    investigation_id: Mapped[str] = mapped_column(
        ForeignKey("investigations.id", ondelete="CASCADE"), index=True
    )
    sequence: Mapped[int] = mapped_column(Integer)
    stage: Mapped[str] = mapped_column(String(50))
    instruction_id: Mapped[str] = mapped_column(String(100))
    summarized_decision: Mapped[str] = mapped_column(Text)
    input_summary: Mapped[dict[str, Any]] = mapped_column(JSON, default=dict)
    output: Mapped[dict[str, Any]] = mapped_column(JSON, default=dict)
    verification_feedback: Mapped[str | None] = mapped_column(Text, nullable=True)


class KnowledgeDocument(Base, TimestampMixin):
    __tablename__ = "knowledge_documents"
    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=uuid_str)
    workspace_id: Mapped[str] = mapped_column(
        ForeignKey("workspaces.id", ondelete="CASCADE"), index=True
    )
    title: Mapped[str] = mapped_column(String(240))
    source_type: Mapped[str] = mapped_column(String(30))
    source_name: Mapped[str] = mapped_column(String(500))
    content_hash: Mapped[str] = mapped_column(String(64))
    chunks: Mapped[list["KnowledgeChunk"]] = relationship(cascade="all, delete-orphan")


class KnowledgeChunk(Base, TimestampMixin):
    __tablename__ = "knowledge_chunks"
    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=uuid_str)
    document_id: Mapped[str] = mapped_column(
        ForeignKey("knowledge_documents.id", ondelete="CASCADE"), index=True
    )
    chunk_index: Mapped[int] = mapped_column(Integer)
    content: Mapped[str] = mapped_column(Text)
    search_terms: Mapped[list[str]] = mapped_column(JSON, default=list)


class EvaluationCase(Base, TimestampMixin):
    __tablename__ = "evaluation_cases"
    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=uuid_str)
    slug: Mapped[str] = mapped_column(String(120), unique=True)
    title: Mapped[str] = mapped_column(String(240))
    ground_truth: Mapped[str] = mapped_column(Text)
    metadata_json: Mapped[dict[str, Any]] = mapped_column(JSON, default=dict)


class EvaluationRun(Base, TimestampMixin):
    __tablename__ = "evaluation_runs"
    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=uuid_str)
    workspace_id: Mapped[str] = mapped_column(
        ForeignKey("workspaces.id", ondelete="CASCADE"), index=True
    )
    status: Mapped[str] = mapped_column(String(30), default="running")
    results: Mapped[dict[str, Any]] = mapped_column(JSON, default=dict)
    duration_ms: Mapped[int] = mapped_column(Integer, default=0)
