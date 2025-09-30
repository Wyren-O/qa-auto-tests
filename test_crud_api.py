import pytest
from fastapi.testclient import TestClient
from app import app 

client = TestClient(app)

@pytest.fixture
def create_user():
    payload = {"name": "Rick", "age": 34}
    response = client.post("/users", json=payload)
    assert response.status_code == 201
    data = response.json()
    user_id = data["id"]
    yield user_id
    # Очистка после теста
    client.delete(f"/users/{user_id}")

def test_get_user(create_user):
    user_id = create_user
    response = client.get(f"/users/{user_id}")
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "Rick"
    assert data["age"] == 34

def test_update_user(create_user):
    user_id = create_user
    new_data = {"name": "Rick Sanchez", "age": 35}
    response = client.put(f"/users/{user_id}", json=new_data)
    assert response.status_code == 200
    data = response.json()
    assert data["age"] == 35
    assert data["name"] == "Rick Sanchez"

def test_delete_user(create_user):
    user_id = create_user
    response = client.delete(f"/users/{user_id}")
    assert response.status_code == 200
    check = client.get(f"/users/{user_id}")
    assert check.status_code == 404

