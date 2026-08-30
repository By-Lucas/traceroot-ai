from datetime import datetime
from typing import Any, Literal

from pydantic import BaseModel, ConfigDict, Field, HttpUrl


class IncidentCreate(BaseModel):
    title: str = Field(min_length=3, max_length=240)
    description: str = Field(min_length=10, max_length=20_000)
    logs: str = Field(default="", max_length=200_000)
    stack_trace: str = Field(default="", max_length=100_000)
    repository_path: str | None = Field(default=None, max_length=500)
    git_url: HttpUrl | None = None
    severity: Literal["low", "medium", "high", "critical"] = "high"


class IncidentResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: str
    title: str
    description: str
    logs: str
    stack_trace: str
    repository_path: str | None
    git_url: str | None
    severity: str
    status: str
    created_at: datetime


class HypothesisOutput(BaseModel):
    id: str
    claim: str
    confidence: float = Field(ge=0, le=1)
    required_evidence: list[str]
    reason: str


class TriageOutput(BaseModel):
    summary: str
    hypotheses: list[HypothesisOutput] = Field(min_length=1, max_length=5)


class EvidenceOutput(BaseModel):
    type: str
    location: str
    content_summary: str
    supports: list[str]
    contradicts: list[str]
    confidence: float = Field(ge=0, le=1)
    content_hash: str = ""


class ReproductionOutput(BaseModel):
    command: str
    exit_code: int
    stdout: str
    stderr: str
    matched_hypotheses: list[str]
    duration_ms: int


class VerificationOutput(BaseModel):
    status: Literal["VERIFIED", "PARTIALLY_VERIFIED", "UNVERIFIED", "REJECTED"]
    root_cause: str | None
    confidence: float = Field(ge=0, le=1)
    rationale: str
    rejected_alternatives: list[str]
    regression_status: str


class InvestigationResponse(BaseModel):
    id: str
    incident_id: str
    status: str
    current_stage: str
    confidence: float
    root_cause: str | None
    report: dict[str, Any]
    duration_ms: int
    token_usage: int
    approximate_cost_usd: float
    hypotheses: list[dict[str, Any]] = []
    evidence: list[dict[str, Any]] = []


class InvestigationListItem(BaseModel):
    id: str
    incident_id: str
    incident_title: str
    severity: str
    status: str
    confidence: float
    root_cause: str | None
    duration_ms: int
    evidence_count: int
    created_at: datetime


class KnowledgeCreate(BaseModel):
    title: str = Field(min_length=2, max_length=240)
    source_type: Literal["markdown", "txt", "json"]
    source_name: str = Field(default="manual", max_length=500)
    content: str = Field(min_length=1, max_length=500_000)


class KnowledgeResponse(BaseModel):
    id: str
    title: str
    source_type: str
    source_name: str
    chunk_count: int
    created_at: datetime
