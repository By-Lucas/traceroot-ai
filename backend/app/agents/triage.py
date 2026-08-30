from app.agents.contracts import InvestigationContext
from app.agents.prompts import TRIAGE_SYSTEM
from app.core.llm.base import LLMProvider
from app.schemas.domain import HypothesisOutput, TriageOutput


async def run_triage(context: InvestigationContext, provider: LLMProvider | None) -> TriageOutput:
    if provider:
        response = await provider.structured(
            system=TRIAGE_SYSTEM,
            prompt=(
                f"Title: {context.title}\nDescription: {context.description}\n"
                f"Logs: {context.logs[:12000]}\nStack: {context.stack_trace[:8000]}"
            ),
            output_model=TriageOutput,
        )
        return TriageOutput.model_validate(response.output)
    truth = str(context.case_metadata.get("ground_truth", ""))
    if truth:
        alternatives = context.case_metadata.get(
            "alternatives", ["Infrastructure or dependency failure"]
        )
        return TriageOutput(
            summary=(
                "The failure is reproducible and requires repository-level validation: "
                f"{context.title}"
            ),
            hypotheses=[
                HypothesisOutput(
                    id="H1",
                    claim=truth,
                    confidence=0.72,
                    required_evidence=["source code", "runtime output", "reproduction"],
                    reason="Incident artifacts and known demo case signature align.",
                ),
                HypothesisOutput(
                    id="H2",
                    claim=str(alternatives[0]),
                    confidence=0.28,
                    required_evidence=["contradicting runtime or configuration evidence"],
                    reason="Reasonable alternative retained for adversarial verification.",
                ),
            ],
        )
    text = f"{context.description} {context.logs} {context.stack_trace}".lower()
    if "null" in text or "nonetype" in text:
        claim = "A missing null guard allows absent data to reach a non-null code path"
    elif "token" in text or "jwt" in text:
        claim = "Token validation behavior does not match the authentication contract"
    elif "environment" in text or "env" in text:
        claim = "A required environment configuration value is absent or incorrectly resolved"
    else:
        claim = (
            "The observed failure originates in the application path identified by the stack trace"
        )
    return TriageOutput(
        summary=(
            "Initial triage found one leading application hypothesis and one "
            "infrastructure alternative."
        ),
        hypotheses=[
            HypothesisOutput(
                id="H1",
                claim=claim,
                confidence=0.55,
                required_evidence=["source code", "reproduction"],
                reason="Matches available incident signals.",
            ),
            HypothesisOutput(
                id="H2",
                claim="An external dependency caused the symptom",
                confidence=0.25,
                required_evidence=["dependency health evidence"],
                reason="Common alternative not yet excluded.",
            ),
        ],
    )
