from datetime import datetime

from sqlalchemy import Column, DateTime, func
from sqlmodel import Field, SQLModel

from enums.reservation import ReservationStatus


class Reservation(SQLModel, table=True):
    __tablename__ = "reservations"

    id: int | None = Field(default=None, primary_key=True)
    user_id: int = Field(foreign_key="users.id", nullable=False)
    schedule_id: int = Field(foreign_key="train_schedules.id", nullable=False)
    seat_id: int = Field(foreign_key="seats.id", nullable=False)
    status: ReservationStatus = Field(default=ReservationStatus.PENDING)
    created_at: datetime = Field(
        sa_column=Column(
            DateTime(timezone=True), nullable=False, server_default=func.now()
        )
    )
