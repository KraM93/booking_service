from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession
from database import get_db
from schemas import EventCreate, SeatResponse
import crud
from crud import book_seat

router = APIRouter(prefix="/events", tags=["Events"])

@router.get("/{event_id}/seats", response_model=list[SeatResponse])
async def get_seats_endpoint(
    event_id: int,
    session: AsyncSession = Depends(get_db)
):
    return await crud.get_available_seats(event_id, session)

@router.post("/", status_code=status.HTTP_201_CREATED)
async def create_event_endpoint(
    payload: EventCreate,
    session: AsyncSession = Depends(get_db)
):
    event_id = await crud.create_event_with_seats(
            title=payload.title,
            start_time=payload.start_time,
            total_rows=payload.total_rows,
            seats_per_row=payload.seats_per_row,
            session=session
    )
    return {
        "status": "ok",
        "message": f"Событие '{payload.title}' и места успешно созданы",
        "event_id": event_id
    }
