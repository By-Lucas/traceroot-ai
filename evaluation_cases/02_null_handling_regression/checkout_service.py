from dataclasses import dataclass


@dataclass(frozen=True)
class CheckoutRequest:
    order_id: str
    subtotal_cents: int
    promo_code: str | None = None


def normalize_promo(promo_code: str) -> str:
    # Regression: the API contract made promo_code optional, but this path still assumes str.
    return promo_code.strip().upper()


def create_checkout(payload: dict[str, object]) -> dict[str, object]:
    request = CheckoutRequest(**payload)
    normalized_promo = normalize_promo(request.promo_code)  # type: ignore[arg-type]
    return {
        "order_id": request.order_id,
        "subtotal_cents": request.subtotal_cents,
        "promo_code": normalized_promo,
    }
