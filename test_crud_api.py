import pytest
import requests
from fastapi.testclient import TestClient
from app import app

client = TestClient(app)
BASE_URL = "http://127.0.0.1:8000/users"

@pytest.fixture
def create_user():
    """Создаём пользователя перед тестом и удаляем после"""
    payload = {"name": "Rick", "age": 34}
    response = requests.post(BASE_URL, json=payload)
    assert response.status_code == 201
    data = response.json()
    user_id = data["id"]
    yield user_id
    # Очистка после теста
    requests.delete(f"{BASE_URL}/{user_id}")

def test_get_user(create_user):
    """Проверяем, что пользователь создаётся и доступен по GET"""
    user_id = create_user
    response = requests.get(f"{BASE_URL}/{user_id}")
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "Rick"
    assert data["age"] == 34

def test_update_user(create_user):
    """Обновляем данные пользователя"""
    user_id = create_user
    new_data = {"name": "Rick Sanchez", "age": 35}
    response = requests.put(f"{BASE_URL}/{user_id}", json=new_data)
    assert response.status_code == 200
    data = response.json()
    assert data["age"] == 35
    assert data["name"] == "Rick Sanchez"

def test_delete_user(create_user):
    """Удаляем пользователя и проверяем 404 после удаления"""
    user_id = create_user
    response = requests.delete(f"{BASE_URL}/{user_id}")
    assert response.status_code == 200
    check = requests.get(f"{BASE_URL}/{user_id}")
    assert check.status_code == 404
