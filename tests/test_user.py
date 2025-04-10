from fastapi.testclient import TestClient
from src.main import app

client = TestClient(app)

# Существующие пользователи
users = [
    {
        'id': 1,
        'name': 'Ivan Ivanov',
        'email': 'i.i.ivanov@mail.com',
    },
    {
        'id': 2,
        'name': 'Petr Petrov',
        'email': 'p.p.petrov@mail.com',
    }
]

def test_get_existed_user():
    '''Получение существующего пользователя'''
    response = client.get("/api/v1/user", params={'email': users[0]['email']})
    assert response.status_code == 200
    assert response.json() == users[0]

def test_get_unexisted_user():
    '''Получение несуществующего пользователя'''
    response = client.get("/api/v1/user", params={'email': 'nonexistent@mail.com'})
    assert response.status_code == 404
    assert response.json() == {"detail": "User not found"}

def test_create_user_with_valid_email():
    '''Создание пользователя с уникальной почтой'''
    new_user = {
        'name': 'Test User',
        'email': 'test.user@mail.com'
    }
    response = client.post("/api/v1/user", json=new_user)
    assert response.status_code == 201
    result = response.json()
    assert isinstance(result, dict)  # проверка, что результат - это словарь
    assert result["name"] == new_user["name"]
    assert result["email"] == new_user["email"]
    assert "id" in result  # Проверка, что id возвращается


def test_create_user_with_valid_email():
    '''Создание пользователя с уникальной почтой'''
    new_user = {
        'name': 'Test User',
        'email': 'test.user@mail.com'
    }
    response = client.post("/api/v1/user", json=new_user)
    assert response.status_code == 201
    user_id = response.json()  # API возвращает просто ID
    assert isinstance(user_id, int)  # Проверка, что это целое число


def test_create_user_with_invalid_email():
    '''Создание пользователя с уже существующей почтой'''
    existing_user = users[0]
    new_user = {
        'name': 'Duplicate Email User',
        'email': existing_user['email']
    }
    response = client.post("/api/v1/user", json=new_user)
    assert response.status_code == 409
    assert response.json() == {"detail": "User with this email already exists"}


def test_delete_user():
    '''Удаление пользователя'''
    user_to_delete = {
        'name': 'To Delete',
        'email': 'delete.me@mail.com'
    }

    # Создаём пользователя
    create_resp = client.post("/api/v1/user", json=user_to_delete)
    assert create_resp.status_code == 201
    user_id = create_resp.json()
    assert isinstance(user_id, int)

    # Удаляем пользователя по email (query параметр!)
    delete_resp = client.delete(f"/api/v1/user", params={"email": user_to_delete["email"]})
    assert delete_resp.status_code == 204


