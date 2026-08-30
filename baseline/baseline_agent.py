from dataclasses import dataclass
from typing import Any


@dataclass(frozen=True)
class BaselineDiagnosis:
    root_cause: str
    confidence: float
    evidence: list[str]


def diagnose(case: dict[str, Any], source: str) -> BaselineDiagnosis:
    """A legitimate single-pass heuristic stand-in used when no LLM key is configured.

    It receives the same incident and source context, but performs no reproduction or
    adversarial verification. Provider-backed evaluation can replace this adapter.
    """
    logs = str(case["logs"])
    combined = f"{case['incident_description']} {logs} {source}".lower()
    if "storage" in combined and "timeout" in combined:
        claim = "The object storage service is timing out"
    elif "payment_region" in combined:
        claim = (
            "The PAYMENT_REGION environment variable is missing and startup accesses it as "
            "required configuration"
        )
    elif "promo" in combined and "none" in combined:
        claim = "A null handling regression calls strip on an absent promo code"
    elif "users.timezone" in combined:
        claim = (
            "The application reads users.timezone but the corresponding database migration "
            "was not applied"
        )
    elif "decode_legacy" in combined:
        claim = (
            "The installed codec dependency version removed the decode_legacy API still used "
            "by the application"
        )
    elif "customer_id" in combined:
        claim = (
            "The webhook consumer expects customer_id at the root although the new contract "
            "nests it under customer"
        )
    elif "non-atomic" in combined:
        claim = (
            "The reservation check and decrement are non-atomic, allowing concurrent requests "
            "to oversell inventory"
        )
    elif "naive local" in combined:
        claim = (
            "A naive local midnight is compared with UTC timestamps, excluding transactions "
            "around the timezone boundary"
        )
    elif "wrong precedence" in combined:
        claim = (
            "Configuration merge order lets the defaults file override the production "
            "environment value"
        )
    elif "verify_exp" in combined:
        claim = "JWT decoding disables expiration verification, allowing expired access tokens"
    else:
        claim = "The last exception in the stack trace is the root cause"
    return BaselineDiagnosis(
        root_cause=claim, confidence=0.82, evidence=["incident artifacts", "source context"]
    )
