from app import reserve

state = {"available": 1}
reserve(state, 1)
reserve(state, 1)
if state["available"] == -1:
    print("TRACEROOT_REPRODUCED: stale reads oversell inventory")
else:
    raise SystemExit(1)
