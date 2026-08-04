from datetime import datetime
from typing import Optional
from pydantic import BaseModel, ConfigDict, EmailStr

class UserCreate(BaseModel):
    email: EmailStr
    password: str

class UserResponse(BaseModel):
    id: int
    email: str
    role: str
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)

class EventCreate(BaseModel):
    title: str
    start_time: datetime
    location: Optional[str] = None
    total_rows: int
    seats_per_row: int

class EventResponse(BaseModel):
    id: int
    title: Optional[str]
    start_time: datetime
    location: Optional[str]

    model_config = ConfigDict(from_attributes=True)

class SeatResponse(BaseModel):
    id: int
    row_number: int
    seat_number: int
    is_booked: bool
    event_id: int

    model_config = ConfigDict(from_attributes=True)

class BookSeatSchema(BaseModel):
    user_id: int

class BookingResponse(BaseModel):
    status: str
    message: str
    seat_id: int
    user_id: int

class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"
