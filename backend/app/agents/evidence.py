import hashlib
from pathlib import Path

from app.agents.contracts import InvestigationContext
from app.core.llm.base import LLMProvider
from app.schemas.domain import EvidenceOutput, TriageOutput
from app.tools.sandbox import RepositorySandbox


async def collect_evidence(
    context: InvestigationContext,
    triage: TriageOutput,
    provider: LLMProvider | None,
    allowed_base: Path,
) -> tuple[list[EvidenceOutput], RepositorySandbox | None]:
    items: list[EvidenceOutput] = []
    runtime = (context.logs + "\n" + context.stack_trace).strip()
    if runtime:
        items.append(
            EvidenceOutput(
                type="runtime",
                location="incident/runtime",
                content_summary=runtime[:800],
                supports=["H1"],
                contradicts=[],
                confidence=0.78,
                content_hash=hashlib.sha256(runtime.encode()).hexdigest(),
            )
        )
    sandbox = None
    if context.repository_path:
        sandbox = RepositorySandbox(Path(context.repository_path), allowed_base)
        evidence_file = str(context.case_metadata.get("evidence_file", "app.py"))
        try:
            content = sandbox.read_file(evidence_file)
            marker = str(context.case_metadata.get("evidence_marker", ""))
            matching_line = next(
                (
                    (number, line.strip())
                    for number, line in enumerate(content.splitlines(), 1)
                    if marker and marker in line
                ),
                None,
            )
            summary = next(
                (line.strip() for line in content.splitlines() if marker and marker in line),
                content[:500],
            )
            items.append(
                EvidenceOutput(
                    type="source_code",
                    location=f"{evidence_file}:{matching_line[0] if matching_line else 1}",
                    content_summary=summary,
                    supports=["H1"],
                    contradicts=["H2"],
                    confidence=0.96,
                    content_hash=sandbox.hash_file(evidence_file),
                )
            )
        except FileNotFoundError:
            pass
    if not items:
        items.append(
            EvidenceOutput(
                type="incident_report",
                location="incident/description",
                content_summary=context.description[:800],
                supports=[],
                contradicts=[],
                confidence=0.3,
                content_hash=hashlib.sha256(context.description.encode()).hexdigest(),
            )
        )
    return items, sandbox
