from app.schemas.domain import EvidenceOutput, ReproductionOutput, TriageOutput, VerificationOutput


def verify(
    triage: TriageOutput, evidence: list[EvidenceOutput], reproduction: ReproductionOutput
) -> VerificationOutput:
    leading = triage.hypotheses[0]
    has_source = any(item.type == "source_code" and "H1" in item.supports for item in evidence)
    has_runtime = any(item.type == "runtime" for item in evidence)
    reproduced = reproduction.exit_code == 0 and "H1" in reproduction.matched_hypotheses
    contradicted = any("H1" in item.contradicts for item in evidence)
    if contradicted:
        status, confidence, root = "REJECTED", 0.1, None
    elif has_source and has_runtime and reproduced:
        status, confidence, root = "VERIFIED", 0.96, leading.claim
    elif has_source and (has_runtime or reproduced):
        status, confidence, root = "PARTIALLY_VERIFIED", 0.7, leading.claim
    else:
        status, confidence, root = "UNVERIFIED", 0.35, None
    alternatives = [hyp.claim for hyp in triage.hypotheses[1:]]
    return VerificationOutput(
        status=status,
        root_cause=root,
        confidence=confidence,
        rationale=(
            f"source={has_source}; runtime={has_runtime}; "
            f"reproduced={reproduced}; contradicted={contradicted}"
        ),
        rejected_alternatives=alternatives if status == "VERIFIED" else [],
        regression_status="NOT_RUN" if status != "VERIFIED" else "REPRODUCTION_CONFIRMED",
    )
