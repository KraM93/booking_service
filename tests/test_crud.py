import pytest
from sqlalchemy.ext.asyncio import AsyncSession
from datetime import datetime

from crud import (
    create_user,
    get_user_by_email,
    create_event_with_seats,
    get_available_seats,
    book_seat,
    get_user_seats,
)
from schemas import EventCreate

async def test_crud_create_and_get_user(db_session: AsyncSession):
    email = "crud_user@test.com"
    new_user = await create_user(email, "hashed_pass_123", db_session)

    assert new_user.id is not None
    assert new_user.email == email

    fetched_user = await get_user_by_email("crud_user@test.com", db_session)
    assert fetched_user is not None
    assert fetched_user.id == new_user.id

    none_user = await get_user_by_email("nonexistent@test.com", db_session)
    assert none_user is None

async def test_crud_create_event_and_seats(db_session: AsyncSession):
    event_in = EventCreate(
        title="Тестовый концерт",
        start_time="2026-10-10T20:00:00",
        total_rows=3,
        seats_per_row=4,
    )
    event_id = await create_event_with_seats(
        event_in.title,
        event_in.start_time,
        event_in.total_rows,
        event_in.seats_per_row,
        db_session,
    )
    assert event_id is not None

    seats = await get_available_seats(event_id, db_session)
    assert len(seats) == 12

async def test_crud_booking_and_user_seats(db_session: AsyncSession):
    new_user = await create_user("buyer@test.com", "hash", db_session)
    event_id = await create_event_with_seats(
        "Кино", datetime.fromisoformat("2026-10-10T20:00:00"), 1, 2, db_session
    )

    seats = await get_available_seats(event_id, db_session)
    seat_to_book = seats[0]

    res = await book_seat(seat_to_book.id, new_user.id, db_session)
    assert res["status"] == "ok"

    user_seats = await get_user_seats(new_user.id, db_session)
    assert len(user_seats) == 1
    assert user_seats[0].id == seat_to_book.id