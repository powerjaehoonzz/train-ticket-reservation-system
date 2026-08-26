from datetime import datetime
from typing import TYPE_CHECKING

from sqlalchemy import Column, DateTime, func
from sqlmodel import Field, Relationship, SQLModel

from enums.seat import SeatClass

if TYPE_CHECKING:
    from models.train import Train
    from models.reservation import Reservation


class Seat(SQLModel, table=True):
    __tablename__ = "seats"

    id: int | None = Field(default=None, primary_key=True)
    train_id: int = Field(foreign_key="trains.id", nullable=False)
    seat_number: str = Field(min_length=1, max_length=10, nullable=False)
    seat_class: SeatClass = Field(nullable=False)
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

    train: "Train" = Relationship(back_populates="seats")
    reservations: list["Reservation"] = Relationship(back_populates="seat")
