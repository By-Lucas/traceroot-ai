def merge(environment, defaults):
    return {**environment, **defaults}  # wrong precedence: defaults win
