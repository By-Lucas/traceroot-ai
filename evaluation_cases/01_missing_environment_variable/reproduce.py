import os

from app import region

os.environ.pop("PAYMENT_REGION", None)
try:
    region()
except KeyError:
    print("TRACEROOT_REPRODUCED: missing PAYMENT_REGION raises KeyError")
else:
    raise SystemExit(1)
