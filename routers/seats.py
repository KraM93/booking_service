from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from database import get_db
from schemas import BookSeatSchema, BookingResponse
from security import get_current_user
from models import User
import crud
from crud import book_seat

router = APIRouter(prefix="/seats", tags=["Seats"])

@router.post("/{seat_id}/book", response_model=BookingResponse)
async def book_seat_endpoint(
    seat_id: int,
    current_user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_db)
):
    return await crud.book_seat(
        seat_id=seat_id,
        user_id=current_user.id,
        session=session
    )