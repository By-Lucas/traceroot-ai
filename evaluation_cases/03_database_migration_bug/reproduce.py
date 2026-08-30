from app import APPLIED_COLUMNS

if "timezone" not in APPLIED_COLUMNS:
    print("TRACEROOT_REPRODUCED: application/schema drift for users.timezone")
else:
    raise SystemExit(1)
