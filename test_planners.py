def auth_client(client):
    email = "planner@example.com"
    password = "strong-password-123"
    client.post("/register", json={"email": email, "password": password})
    client.post("/login", json={"email": email, "password": password})


def test_home_planner(client):
    auth_client(client)
    payload = {
        "budget": 50000,
        "rooms": ["Living Room"],
        "style": "modern",
        "location": "India",
        "items": [
            {"category": "Lighting", "item": "LED ceiling light", "quantity": 2, "max_budget": 3000}
        ]
    }
    response = client.post("/generate-home", json=payload)
    assert response.status_code == 200
    body = response.json()
    assert body["result"]["planner"] == "home"
    assert len(body["result"]["recommendations"]) >= 1


def test_party_planner(client):
    auth_client(client)
    payload = {
        "budget": 100000,
        "guests": 40,
        "event_type": "birthday",
        "venue": "indoor hall",
        "city": "Chennai",
        "preferences": "vegetarian"
    }
    response = client.post("/generate-party", json=payload)
    assert response.status_code == 200
    assert response.json()["result"]["planner"] == "party"
