from datetime import datetime

from sqlalchemy import Column, DateTime, func
from sqlmodel import Field, SQLModel

from backend.enums.user import UserRole


class User(SQLModel, table=True):
    __tablename__ = "users"

    id: int | None = Field(default=None, primary_key=True)
    email: str = Field(max_length=255, unique=True, nullable=False)
    hashed_password: str = Field(max_length=255, nullable=False)
    name: str = Field(max_length=50, nullable=False)
    role: UserRole = Field(default=UserRole.USER, nullable=False)
    created_at: datetime = Field(
        sa_column=Column(
            DateTime(timezone=True), nullable=False, server_default=func.now()
        ),
    )
    updated_at: datetime = Field(
        sa_column=Column(
            DateTime(timezone=True),
            nullable=False,
            server_default=func.now(),
            onupdate=func.now(),
        ),
    )
