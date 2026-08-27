from datetime import datetime
from typing import TYPE_CHECKING

from sqlalchemy import Column, DateTime, UniqueConstraint, func
from sqlmodel import Field, Relationship, SQLModel

from enums.train import TrainType

if TYPE_CHECKING:
    from models.train_schedule import TrainSchedule
    from models.seat import Seat


class Train(SQLModel, table=True):
    __tablename__ = "trains"

    __table_args__ = UniqueConstraint(
        "train_type", "train_number", name="uq_train_type_number"
    )

    id: int | None = Field(default=None, primary_key=True)
    train_type: TrainType = Field(nullable=False)
    train_number: str = Field(min_length=1, max_length=10, nullable=False)
    capacity: int = Field(gt=0, multiple_of=4, nullable=False)
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

    schedules: list["TrainSchedule"] = Relationship(back_populates="train")
    seats: list["Seat"] = Relationship(back_populates="train")
