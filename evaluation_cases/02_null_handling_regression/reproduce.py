from checkout_service import create_checkout


production_payload = {
    "order_id": "ord-1042",
    "subtotal_cents": 12900,
    # promo_code is optional and is legitimately omitted by the client.
}

try:
    create_checkout(production_payload)
except AttributeError as error:
    assert "strip" in str(error)
    print("TRACEROOT_REPRODUCED: optional promo_code reaches str.strip as None")
else:
    raise SystemExit("Expected checkout to reproduce the production AttributeError")
