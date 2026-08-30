# Incident response evidence standard

A production root-cause statement must identify the failing mechanism, the affected code or configuration and the observation that demonstrates causality. A final stack frame is a symptom until reproduced.

Never execute a production change directly from an automated diagnosis. Preserve request IDs and artifact hashes, reject evidence without provenance and require an engineer to approve remediation.
