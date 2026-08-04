from fastapi import FastAPI
from routers import events, seats, users

app = FastAPI(title="Seat Booking API")

app.include_router(events.router)
app.include_router(seats.router)
app.include_router(users.router)

@app.get("/")
async def root():
    return {"message": "Booking API работает. Перейдите на /docs"}