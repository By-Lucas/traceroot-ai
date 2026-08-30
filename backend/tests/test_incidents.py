from fastapi.testclient import TestClient


def payload(case: str = "02_null_handling_regression") -> dict[str, str]:
    return {
        "title": "Discount API returns 500",
        "description": "Orders without promo codes now fail consistently.",
        "logs": "AttributeError: 'NoneType' object has no attribute 'strip'",
        "stack_trace": "app.py:2 in normalize",
        "repository_path": case,
        "severity": "high",
    }


def test_golden_investigation_returns_verified_report(
    client: TestClient, auth_headers: dict[str, str]
) -> None:
    created = client.post("/api/v1/incidents", json=payload(), headers=auth_headers)
    assert created.status_code == 201
    result = client.post(
        f"/api/v1/incidents/{created.json()['id']}/investigate", headers=auth_headers
    )
    assert result.status_code == 201
    body = result.json()
    assert body["status"] == "VERIFIED"
    assert body["root_cause"] and len(body["evidence"]) >= 2
    trajectory = client.get(f"/api/v1/investigations/{body['id']}/trajectory", headers=auth_headers)
    assert [step["stage"] for step in trajectory.json()] == [
        "triage",
        "evidence",
        "reproduction",
        "verification",
    ]
    report = client.get(f"/api/v1/investigations/{body['id']}/report", headers=auth_headers)
    assert report.json()["human_approval_requirement"].startswith("Required")


def test_without_repository_is_unverified(client: TestClient, auth_headers: dict[str, str]) -> None:
    request = payload()
    request["repository_path"] = ""
    created = client.post("/api/v1/incidents", json=request, headers=auth_headers).json()
    result = client.post(f"/api/v1/incidents/{created['id']}/investigate", headers=auth_headers)
    assert result.status_code == 201
    assert result.json()["status"] == "UNVERIFIED"
    assert result.json()["root_cause"] is None


def test_user_cannot_read_another_workspace(
    client: TestClient, auth_headers: dict[str, str]
) -> None:
    incident = client.post("/api/v1/incidents", json=payload(), headers=auth_headers).json()
    second = client.post(
        "/api/v1/auth/register",
        json={"email": "other@example.com", "password": "secure-pass-456", "display_name": "Grace"},
    ).json()
    headers = {"Authorization": f"Bearer {second['access_token']}"}
    assert client.get(f"/api/v1/incidents/{incident['id']}", headers=headers).status_code == 404
