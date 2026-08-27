from datetime import datetime
from typing import TYPE_CHECKING

from sqlalchemy import Column, DateTime, Index, func, text
from sqlmodel import Field, Relationship, SQLModel

from enums.reservation import ReservationStatus

if TYPE_CHECKING:
    from models.user import User
    from models.train_schedule import TrainSchedule
    from models.seat import Seat


class Reservation(SQLModel, table=True):
    __tablename__ = "reservations"

    __table_args__ = (
        Index(
            "uq_active_schedule_seat",
            "schedule_id",
            "seat_id",
            unique=True,
            postgresql_where=text("status != 'CANCELLED'"),
        ),
    )

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

    user: "User" = Relationship(back_populates="reservations")
    schedule: "TrainSchedule" = Relationship(back_populates="reservations")
    seat: "Seat" = Relationship(back_populates="reservations")
