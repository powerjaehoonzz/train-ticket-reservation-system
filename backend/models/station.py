from datetime import datetime

from sqlalchemy import Column, DateTime, func
from sqlmodel import Field, SQLModel

from enums.station import Region


class Station(SQLModel, table=True):
    __tablename__ = "stations"

    id: int | None = Field(default=None, primary_key=True)
    name: str = Field(max_length=50, unique=True, nullable=False)
    code: str = Field(max_length=5, unique=True, nullable=False)
    city: str = Field(max_length=50, nullable=False)
    region: Region = Field(nullable=False)
    created_at: datetime = Field(
        sa_column=Column(
            DateTime(timezone=True), nullable=False, server_default=func.now()
        )
    )
    updated_at: datetime = Field(
        sa_column=Column(
            DateTime(timezone=True),
            nullable=False,
            server_default=func.now(),
            onupdate=func.now(),
        )
    )
