def reserve(state, observed):
    if observed > 0:
        state["available"] -= 1  # non-atomic check uses stale observed value
