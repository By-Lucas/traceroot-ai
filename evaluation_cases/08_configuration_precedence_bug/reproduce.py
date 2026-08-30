from app import merge

result = merge({"endpoint": "prod"}, {"endpoint": "staging"})
if result["endpoint"] == "staging":
    print("TRACEROOT_REPRODUCED: defaults override environment")
else:
    raise SystemExit(1)
