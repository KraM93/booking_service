import pytest
from httpx import AsyncClient

async def get_auth_headers(client: AsyncClient, email: str = "user@test.com") -> dict:
    await client.post("/users/", json={"email": email, "password": "password123"})
    login_res = await client.post(
        "/users/login",
        data={"username": email, "password": "password123"}
    )
    token = login_res.json()["access_token"]
    return {"Authorization": f"Bearer {token}"}

async def test_create_event(client: AsyncClient):
    response = await client.post(
        "/events/",
        json={
            "title": "Рок-концерт",
            "start_time": "2026-08-15T19:00:00",
            "total_rows": 2,
            "seats_per_row": 3
        }
    )
    assert response.status_code == 201
    assert "event_id" in response.json()

async def test_book_seat_success(client: AsyncClient):
    headers = await get_auth_headers(client)

    event_res = await client.post(
        "/events/",
        json={
            "title": "Спектакль",
            "start_time": "2026-09-01T18:00:00",
            "total_rows": 2,
            "seats_per_row": 3
        }
    )
    event_id = event_res.json()["event_id"]

    seats_res = await client.get(f"/events/{event_id}/seats")
    seats = seats_res.json()
    first_seat_id = seats[0]["id"]

    book_res = await client.post(f"/seats/{first_seat_id}/book", headers=headers)
    assert book_res.status_code == 200
    assert book_res.json()["status"] == "ok"

async def test_book_seat_unauthorized(client: AsyncClient):
    response = await client.post("/seats/1/book")
    assert response.status_code == 401