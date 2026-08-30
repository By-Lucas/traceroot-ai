from checkout_service import create_checkout


def test_checkout_with_promo_still_works() -> None:
    result = create_checkout(
        {"order_id": "ord-1041", "subtotal_cents": 12900, "promo_code": " save10 "}
    )
    assert result["promo_code"] == "SAVE10"


def test_production_failure_is_reproducible() -> None:
    try:
        create_checkout({"order_id": "ord-1042", "subtotal_cents": 12900})
    except AttributeError as error:
        assert "strip" in str(error)
    else:
        raise AssertionError("Missing promo_code should reproduce the current regression")
