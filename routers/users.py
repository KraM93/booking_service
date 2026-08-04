from fastapi import APIRouter, Depends, HTTPException, status, Request
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession
from schemas import UserCreate, UserResponse, SeatResponse, Token
from crud import create_user, get_user_by_email, get_user_seats
from database import get_db
from security import get_password_hash, verify_password, create_access_token
from limiter import limiter
from logger import logger

router = APIRouter(prefix="/users", tags=["Users"])

@router.post("/", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
@limiter.limit("5/minute")
async def register_user(
    user_data: UserCreate,
    request: Request,
    session: AsyncSession = Depends(get_db)
):
    logger.info(f"Попытка регистрации пользователя: {user_data.email}")
    existing_user = await get_user_by_email(user_data.email, session)
    if existing_user:
        raise HTTPException(
            status_code=400,
            detail="Пользователь с таким e-mail уже существует"
        )

    hashed_password = get_password_hash(user_data.password)

    new_user = await create_user(
        email=user_data.email,
        password_hash=hashed_password,
        session=session
    )

    return new_user

@router.post("/login", response_model=Token)
@limiter.limit("5/minute")
async def login_user(
    request: Request,
    form_data: OAuth2PasswordRequestForm = Depends(),
    session: AsyncSession = Depends(get_db)
):
    logger.info(f"Попытка входа пользователя: {form_data.username}")
    user = await get_user_by_email(form_data.username, session)

    if not user or not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Неверный email или пароль",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token = create_access_token(data={"sub": str(user.id)})
    return {"access_token": access_token, "token_type": "bearer"}

@router.get("/{user_id}/seats", response_model=list[SeatResponse])
async def get_user_seats_endpoint(
    user_id: int,
    session: AsyncSession = Depends(get_db)
):
    user_seats = await get_user_seats(user_id=user_id, session=session)
    return user_seats