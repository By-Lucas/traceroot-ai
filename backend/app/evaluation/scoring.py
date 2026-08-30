from typing import Any


def normalize(value: str | None) -> str:
    return " ".join((value or "").lower().strip().rstrip(".").split())


def score_case(
    *,
    predicted: str | None,
    ground_truth: str,
    evidence_valid: bool,
    verification_supports: bool,
    reproduction_succeeded: bool,
    confidence: float,
) -> dict[str, Any]:
    root_cause_correct = normalize(predicted) == normalize(ground_truth)
    verified_correct = root_cause_correct and evidence_valid and verification_supports
    false_confident = confidence >= 0.8 and not root_cause_correct
    return {
        "root_cause_correct": root_cause_correct,
        "evidence_valid": evidence_valid,
        "verification_supports": verification_supports,
        "reproduction_succeeded": reproduction_succeeded,
        "verified_root_cause_correct": verified_correct,
        "false_confident": false_confident,
    }


def aggregate(rows: list[dict[str, Any]]) -> dict[str, float | int]:
    total = len(rows)
    if total == 0:
        return {"cases": 0}

    def rate(key: str) -> float:
        return round(sum(bool(row[key]) for row in rows) / total, 4)

    valid_evidence = sum(bool(row["evidence_valid"]) for row in rows)
    return {
        "cases": total,
        "raw_root_cause_accuracy": rate("root_cause_correct"),
        "vrca": rate("verified_root_cause_correct"),
        "evidence_precision": round(valid_evidence / total, 4),
        "reproduction_success_rate": rate("reproduction_succeeded"),
        "false_confident_diagnosis_rate": rate("false_confident"),
    }
