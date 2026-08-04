from fastapi import FastAPI, Request
from slowapi import _rate_limit_exceeded_handler
from slowapi.errors import RateLimitExceeded
from limiter import limiter
from logger import logger
from routers import events, seats, users

app = FastAPI(title="Seat Booking API")
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)
app.include_router(events.router)
app.include_router(seats.router)
app.include_router(users.router)

@app.middleware("http")
async def log_request(request: Request, call_next):
    logger.info(f"Start request: {request.method} {request.url.path}")
    response = await call_next(request)
    logger.info(
        f"Completed: {request.method} {request.url.path} | Status: {response.status_code}"
    )
    return response

@app.get("/")
async def root():
    return {"message": "Booking API работает. Перейдите на /docs"}