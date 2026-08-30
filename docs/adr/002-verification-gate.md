# ADR 002: Independent verification gate

Status: Accepted

Only the verification stage may assign `VERIFIED`, `PARTIALLY_VERIFIED`, `UNVERIFIED` or `REJECTED`. Triage confidence is advisory. `VERIFIED` requires supporting source, runtime and successful reproduction evidence without a contradiction. Production deployment always requires human approval.
