from datetime import UTC, datetime, timedelta
from typing import Any, Literal
import uuid

import jwt
from jwt.exceptions import InvalidTokenError

from core.config import settings

TokenType = Literal["access", "refresh"]


class JWTService:
    def __init__(self) -> None:
        self._secret_key = settings.SECRET_KEY
        self._algorithm = settings.ALGORITHM
        self._access_token_expire_minutes = settings.ACCESS_TOKEN_EXPIRE_MINUTES
        self._refresh_token_expire_days = settings.REFRESH_TOKEN_EXPIRE_DAYS

    def issue(
        self,
        *,
        token_type: TokenType,
        subject: str,
        expires_delta: timedelta | None = None,
    ) -> str:
        now = datetime.now(UTC)

        if expires_delta is None:
            if token_type == "access":
                expires_delta = timedelta(minutes=self._access_token_expire_minutes)
            else:
                expires_delta = timedelta(days=self._refresh_token_expire_days)

        expire = now + expires_delta

        payload = {
            "sub": subject,
            "typ": token_type,
            "jti": str(uuid.uuid4()),
            "iat": int(now.timestamp()),
            "exp": int(expire.timestamp()),
        }

        return jwt.encode(payload, self._secret_key, algorithm=self._algorithm)

    def decode_and_verify(
        self, token: str, *, expected_type: TokenType
    ) -> dict[str, Any]:
        payload = jwt.decode(
            token,
            self._secret_key,
            algorithms=[self._algorithm],
            options={"require": ["sub", "typ", "jti", "iat", "exp"]},
        )

        if payload["typ"] != expected_type:
            raise InvalidTokenError(f"Expected {expected_type} token.")

        return payload


jwt_service = JWTService()
