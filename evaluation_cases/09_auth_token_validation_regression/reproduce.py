from app import JWT_OPTIONS

if JWT_OPTIONS["verify_exp"] is False:
    print("TRACEROOT_REPRODUCED: expired token verification disabled")
else:
    raise SystemExit(1)
