from app import INSTALLED_APIS, REQUIRED_API

if REQUIRED_API not in INSTALLED_APIS:
    print("TRACEROOT_REPRODUCED: dependency API mismatch")
else:
    raise SystemExit(1)
