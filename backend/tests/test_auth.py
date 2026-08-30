from fastapi.testclient import TestClient


def test_register_login_refresh_and_me(client: TestClient) -> None:
    registered = client.post(
        "/api/v1/auth/register",
        json={
            "email": "ada@example.com",
            "password": "a-secure-password",
            "display_name": "Ada Lovelace",
        },
    )
    assert registered.status_code == 201
    tokens = registered.json()
    me = client.get(
        "/api/v1/auth/me", headers={"Authorization": f"Bearer {tokens['access_token']}"}
    )
    assert me.status_code == 200
    assert me.json()["email"] == "ada@example.com"
    assert (
        client.post(
            "/api/v1/auth/refresh", json={"refresh_token": tokens["refresh_token"]}
        ).status_code
        == 200
    )
    assert (
        client.post(
            "/api/v1/auth/login", json={"email": "ada@example.com", "password": "a-secure-password"}
        ).status_code
        == 200
    )


def test_duplicate_registration_and_wrong_password(client: TestClient) -> None:
    payload = {"email": "ada@example.com", "password": "a-secure-password", "display_name": "Ada"}
    assert client.post("/api/v1/auth/register", json=payload).status_code == 201
    assert client.post("/api/v1/auth/register", json=payload).status_code == 409
    assert (
        client.post(
            "/api/v1/auth/login", json={"email": "ada@example.com", "password": "wrong"}
        ).status_code
        == 401
    )


def test_protected_route_requires_access_token(client: TestClient) -> None:
    assert client.get("/api/v1/incidents").status_code == 401
