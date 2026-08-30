from app import customer_id

try:
    customer_id({"customer": {"id": "cus_1"}})
except KeyError:
    print("TRACEROOT_REPRODUCED: v2 payload violates old consumer assumption")
else:
    raise SystemExit(1)
