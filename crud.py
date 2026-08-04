import asyncio
from database import async_sessionmaker, get_db
from models import User, Seat, Event, Booking
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from datetime import datetime
from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel, ConfigDict

async def get_db():
    async with async_sessionmaker() as session:
        yield session

async def create_user(email: str, password_hash: str, session: AsyncSession):
    new_user = User(email=email, hashed_password=password_hash)

    session.add(new_user)

    await session.commit()

    print(f"Пользователь {new_user.id} создан!")

    return new_user

async def get_user_by_email(email: str, session: AsyncSession):
    query = select(User).where(User.email == email)

    result = await session.execute(query)

    user = result.scalar_one_or_none()
    return user

async def update_user_password(email: str, new_password_hash: str, session: AsyncSession):
    query = select(User).where(User.email == email)
    result = await session.execute(query)
    user = result.scalar_one_or_none()

    if user:
        user.hashed_password = new_password_hash
        await session.commit()
        print(f"Пароль для {email} обновлен")
    else:
        print("Пользователь не найден")

async def delete_user(email: str, session: AsyncSession):
    query = select(User).where(User.email == email)
    result = await session.execute(query)
    user = result.scalar_one_or_none()

    if user:
        await session.delete(user)
        await session.commit()
        print(f"Пользователь {email} удален")
    else:
        print("Пользователь не найден.")


async def create_event_with_seats(
    title: str,
    start_time: datetime,
    total_rows: int,
    seats_per_row: int,
    session: AsyncSession
) -> int:
    event = Event(
        title = title,
        start_time = start_time,
        )
    session.add(event)
    await session.flush()
    seats = []
    for row in range(1, total_rows + 1):
        for seat in range(1, seats_per_row + 1):
            new_seat = Seat(
                event_id = event.id,
                row_number = row,
                seat_number = seat
            )
            seats.append(new_seat)
    session.add_all(seats)
    await session.commit()
    print(f"Создано событие '{title}' и {len(seats)} мест!")
    return event.id

async def get_available_seats(event_id: int, session: AsyncSession):
    query = select(Seat).where(
        Seat.event_id == event_id,
        Seat.is_booked == False
    )

    result = await session.execute(query)
    seats = result.scalars().all()
    return seats

async def book_seat(
    seat_id: int,
    user_id: int,
    session: AsyncSession
) -> dict:
    user_query = select(User).where(User.id == user_id)
    user_result = await session.execute(user_query)
    user = user_result.scalar_one_or_none()

    if user is None:
        raise HTTPException(
            status_code=404,
            detail=f"Пользователь с id={user_id} не найден"
        )
    seat_query = select(Seat
                ).where(Seat.id == seat_id
                ).with_for_update()
    seat_result = await session.execute(seat_query)
    seat = seat_result.scalar_one_or_none()

    if seat is None:
        raise HTTPException(
            status_code=404,
            detail="Место не найдено"
        )
    if seat.is_booked:
        raise HTTPException(
            status_code=400,
            detail=f"Место {seat_id} уже забронировано"
        )
    
    seat.is_booked = True
    new_booking = Booking(
        user_id=user_id,
        seat_id=seat_id,
        status="confirmed"
    )
    session.add(new_booking)
    await session.commit()

    return {
        "status": "ok",
        "message": f"Место {seat_id} успешно забронировано пользователем {user_id}",
        "seat_id": seat_id,
        "user_id": user_id
    }

async def get_user_seats(
        user_id: int,
        session: AsyncSession
):
    query = (
        select(Seat)
        .join(Booking, Seat.id == Booking.seat_id)
        .where(Booking.user_id == user_id)
    )
    result = await session.execute(query)
    return result.scalars().all()


async def main():
    async with async_sessionmaker() as session:
        test_email = "crud_test@example.com"
        await create_user(test_email, "pass123", session)
        user = await get_user_by_email(test_email, session)
        print(f"Найден: {user.email} Пароль: {user.hashed_password}")
        await update_user_password(test_email, "new_secret_pass_456", session)
        await delete_user(test_email, session)
        event_id = await create_event_with_seats(
            "concert",
            datetime(2026, 4, 3, 19, 0),
            2,
            5,
            session
        )
        seats = await get_available_seats(event_id, session)
        print(f"Свободных мест для события ID={event_id}: {len(seats)}")

if __name__ == "__main__":
    asyncio.run(main())