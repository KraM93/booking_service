from fastapi import APIRouter, Depends, status, Query
from sqlalchemy.ext.asyncio import AsyncSession
from database import get_db
from schemas import EventCreate, SeatResponse, EventResponse
import crud

router = APIRouter(prefix="/events", tags=["Events"])

@router.get("/", response_model=list[EventResponse])
async def get_events_endpoint(
    limit: int = Query(
        10, ge=1, le=100, description="Количество возвращаемых записей (1-100)"
    ),
    offset: int = Query(0, ge=0, description="Смещение (пропуск записей)"),
    title: str
    | None = Query(
        None, description="Фильтр по названию мероприятия (поиск по подстроке)"
    ),
    session: AsyncSession = Depends(get_db)
):
    return await crud.get_events(
        session=session, limit=limit, offset=offset, title=title
    )

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