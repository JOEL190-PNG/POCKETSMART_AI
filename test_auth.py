def test_register_login_session(client):
    email = "test@example.com"
    password = "strong-password-123"

    r = client.post("/register", json={"email": email, "password": password})
    assert r.status_code in (200, 409)

    r = client.post("/login", json={"email": email, "password": password})
    assert r.status_code == 200
    assert "access_token" in r.cookies

    r = client.get("/session-info")
    assert r.status_code == 200
    assert r.json()["authenticated"] is True
