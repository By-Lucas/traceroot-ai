from app.evaluation.scoring import aggregate, score_case


def test_vrca_requires_claim_evidence_and_verification() -> None:
    row = score_case(
        predicted="Cause A",
        ground_truth="Cause A",
        evidence_valid=True,
        verification_supports=False,
        reproduction_succeeded=True,
        confidence=0.9,
    )
    assert row["root_cause_correct"] is True and row["verified_root_cause_correct"] is False


def test_false_confident_diagnosis() -> None:
    row = score_case(
        predicted="Cause B",
        ground_truth="Cause A",
        evidence_valid=False,
        verification_supports=False,
        reproduction_succeeded=False,
        confidence=0.91,
    )
    assert row["false_confident"] is True
    assert aggregate([row])["false_confident_diagnosis_rate"] == 1.0
