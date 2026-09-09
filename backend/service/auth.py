from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from core.jwt import jwt_service
from schemas.auth import Token
from models.user import User
from schemas.user import UserCreate
from repository.user import UserRepository
from core.security import password_hasher


class AuthService:
    def __init__(
        self,
        session: AsyncSession,
        user_repository: UserRepository,
    ) -> None:
        self._session = session
        self._user_repository = user_repository

    async def register(self, user_in: UserCreate) -> User:
        existing_user = await self._user_repository.get_by_email(user_in.email)

        if existing_user is not None:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="이미 사용중인 이메일입니다.",
            )

        user = User(
            email=user_in.email,
            hashed_password=password_hasher.hash(user_in.password),
            name=user_in.name,
        )

        try:
            await self._user_repository.create(user)
            await self._session.commit()
        except Exception:
            await self._session.rollback()
            raise

        return user

    async def login(self, email: str, password: str) -> Token:
        user = await self._user_repository.get_by_email(email)

        if user is None:
            password_hasher.verify_dummy(password)
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="이메일 또는 비밀번호가 올바르지 않습니다.",
            )

        valid, new_hash = password_hasher.verify_and_update(
            password, user.hashed_password
        )

        if not valid:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="이메일 또는 비밀번호가 올바르지 않습니다.",
            )

        if new_hash is not None:
            user.hashed_password = new_hash

            try:
                await self._session.commit()
            except Exception:
                await self._session.rollback()
                raise

        access_token = jwt_service.issue(token_type="access", subject=str(user.id))

        refresh_token = jwt_service.issue(token_type="refresh", subject=str(user.id))

        return Token(access_token=access_token, refresh_token=refresh_token)
