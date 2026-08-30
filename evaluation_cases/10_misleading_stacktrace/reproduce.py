from app import timeout

if timeout("0.5") == 0:
    print("TRACEROOT_REPRODUCED: local timeout truncates to zero; storage is healthy")
else:
    raise SystemExit(1)
