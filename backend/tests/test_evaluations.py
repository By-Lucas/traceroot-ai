from fastapi.testclient import TestClient


def test_evaluation_executes_mounted_cases(
    client: TestClient, auth_headers: dict[str, str]
) -> None:
    started = client.post("/api/v1/evaluations", headers=auth_headers)
    assert started.status_code == 202

    result = client.get(
        f"/api/v1/evaluations/{started.json()['id']}", headers=auth_headers
    )
    assert result.status_code == 200
    body = result.json()
    assert body["status"] == "completed"
    assert body["results"]["metrics"]["cases"] == 10
    null_case = next(
        item
        for item in body["results"]["cases"]
        if item["slug"] == "02_null_handling_regression"
    )
    assert null_case["evidence_found"] is True
    assert null_case["reproduced"] is True
    assert null_case["status"] == "VERIFIED"
