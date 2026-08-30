from fastapi.testclient import TestClient


def test_ingest_and_list_document(client: TestClient, auth_headers: dict[str, str]) -> None:
    body = {
        "title": "Payments runbook",
        "source_type": "markdown",
        "source_name": "runbook.md",
        "content": (
            "# Payments\n\nCheck request IDs before retrying.\n\n"
            "Never replay a charge without idempotency."
        ),
    }
    created = client.post("/api/v1/knowledge", json=body, headers=auth_headers)
    assert created.status_code == 201 and created.json()["chunk_count"] >= 1
    assert len(client.get("/api/v1/knowledge", headers=auth_headers).json()) == 1
    assert client.post("/api/v1/knowledge", json=body, headers=auth_headers).status_code == 409
