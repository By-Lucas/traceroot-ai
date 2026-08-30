from app import normalize

try:
    normalize(None)
except AttributeError:
    print("TRACEROOT_REPRODUCED: None promo reaches strip")
else:
    raise SystemExit(1)
