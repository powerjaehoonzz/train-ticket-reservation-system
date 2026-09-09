from fastapi import APIRouter, Depends, status

from schemas.auth import LoginRequest, Token
from core.dependencies import get_auth_service
from service.auth import AuthService
from schemas.user import UserCreate, UserRead

router = APIRouter(
    prefix="/auth",
    tags=["Auth"],
)


@router.post("/register", response_model=UserRead, status_code=status.HTTP_201_CREATED)
async def register(
    user_in: UserCreate, auth_service: AuthService = Depends(get_auth_service)
) -> UserRead:
    return await auth_service.register(user_in)


@router.post("/login", response_model=Token)
async def login(
    login_in: LoginRequest, auth_service: AuthService = Depends(get_auth_service)
) -> Token:
    return await auth_service.login(login_in.email, login_in.password)
