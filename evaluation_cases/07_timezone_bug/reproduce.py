from app import day_start

if day_start().tzinfo is None:
    print("TRACEROOT_REPRODUCED: naive local boundary has no timezone")
else:
    raise SystemExit(1)
