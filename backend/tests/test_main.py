import pytest
from fastapi.testclient import TestClient
from app.main import app
from app import crud
import uuid

@pytest.fixture
def client():
    with TestClient(app) as c:
        yield c

def test_create_user(client):
    unique_suffix = uuid.uuid4().hex[:6]
    username = f"testuser_{unique_suffix}"
    email = f"{username}@example.com"
    response = client.post(
        "/users/",
        json={"username": username, "email": email, "password": "testpass"}
    )
    assert response.status_code == 200, f"Response: {response.json()}"
    data = response.json()
    assert data["username"] == username
    assert data["email"] == email

def test_login_and_access_token(client):
    client.post("/users/", json={"username": "loginuser", "email": "login@example.com", "password": "secret"})

    response = client.post(
        "/token",
        data={"username": "loginuser", "password": "secret"},
        headers={"Content-Type": "application/x-www-form-urlencoded"}
    )
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert data["token_type"] == "bearer"

def test_create_sweet_requires_auth(client):
    sweet_data = {
        "name": "Candy",
        "description": "Yummy",
        "price": 50,
        "category": "Sugar",
        "quantity": 10
    }
    response = client.post("/sweets/", json=sweet_data)
    assert response.status_code == 401

def test_create_and_get_sweets(client):
    client.post("/users/", json={"username": "sweetuser", "email": "sweet@example.com", "password": "pass"})
    login_response = client.post(
        "/token",
        data={"username": "sweetuser", "password": "pass"},
        headers={"Content-Type": "application/x-www-form-urlencoded"}
    )
    token = login_response.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}
    sweet_data = {
        "name": "Candy",
        "description": "Yummy",
        "price": 50,
        "category": "Sugar",
        "quantity": 10
    }
    create_response = client.post("/sweets/", json=sweet_data, headers=headers)
    assert create_response.status_code == 200
    sweet = create_response.json()
    assert sweet["name"] == sweet_data["name"]
    get_response = client.get("/sweets/")
    assert get_response.status_code == 200
    sweets = get_response.json()
    assert any(s["name"] == "Candy" for s in sweets)