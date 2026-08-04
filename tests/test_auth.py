import pytest
from httpx import AsyncClient

async def test_register_user_success(client: AsyncClient):
    response = await client.post(
        "/users/",
        json={"email": "testuser@example.com", "password": "securepassword123"}
    )
    assert response.status_code == 201
    data = response.json()
    assert data["email"] == "testuser@example.com"
    assert "id" in data

async def test_register_duplicate_email(client: AsyncClient):
    user_data = {"email": "duplicate@example.com", "password": "pass"}

    await client.post("/users/", json=user_data)

    response = await client.post("/users/", json=user_data)
    assert response.status_code == 400
    assert response.json()["detail"] == "Пользователь с таким e-mail уже существует"

async def test_login_success(client: AsyncClient):
    await client.post(
        "/users/",
        json={"email": "loginuser@example.com", "password": "mypassword"}
    )

    response = await client.post(
        "/users/login",
        data={"username": "loginuser@example.com", "password": "mypassword"}
    )
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert data["token_type"] == "bearer"