from datetime import datetime
from typing import TYPE_CHECKING

from sqlalchemy import Column, DateTime, func
from sqlmodel import Field, Relationship, SQLModel

from enums.station import Region

if TYPE_CHECKING:
    from models.train_schedule import TrainSchedule


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

    departure_schedules: list["TrainSchedule"] = Relationship(
        back_populates="departure_station",
        sa_relationship_kwargs={"foreign_keys": "[TrainSchedule.departure_station_id]"},
    )
    arrival_schedules: list["TrainSchedule"] = Relationship(
        back_populates="arrival_station",
        sa_relationship_kwargs={"foreign_keys": "[TrainSchedule.arrival_station_id]"},
    )
