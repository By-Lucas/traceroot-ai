# Optional promo code regression

This fixture models a checkout service whose public request contract permits an
omitted promo code. A refactored normalization path still calls `str.strip`
without handling `None`, reproducing the production 500.

`reproduce.py` sends the same payload shape reported by the incident and exits
successfully only when the expected failure signature is observed.
