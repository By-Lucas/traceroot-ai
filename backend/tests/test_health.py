from fastapi.testclient import TestClient


def test_health_ready_and_openapi(client: TestClient) -> None:
    assert client.get("/health").json()["status"] == "ok"
    assert client.get("/ready").json()["database"] == "connected"
    assert "/api/v1/incidents" in client.get("/openapi.json").json()["paths"]
