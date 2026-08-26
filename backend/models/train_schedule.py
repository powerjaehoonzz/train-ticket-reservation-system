from datetime import datetime
from typing import TYPE_CHECKING

from sqlalchemy import Column, DateTime, func
from sqlmodel import Field, Relationship, SQLModel

if TYPE_CHECKING:
    from models.train import Train
    from models.station import Station
    from models.reservation import Reservation


class TrainSchedule(SQLModel, table=True):
    __tablename__ = "train_schedules"

    id: int | None = Field(default=None, primary_key=True)
    train_id: int = Field(foreign_key="trains.id", nullable=False)
    departure_station_id: int = Field(foreign_key="stations.id", nullable=False)
    arrival_station_id: int = Field(foreign_key="stations.id", nullable=False)
    departure_time: datetime = Field(
        sa_column=Column(DateTime(timezone=True), nullable=False)
    )
    arrival_time: datetime = Field(
        sa_column=Column(DateTime(timezone=True), nullable=False)
    )
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

    train: "Train" = Relationship(back_populates="schedules")
    departure_station: "Station" = Relationship(
        back_populates="departure_schedules",
        sa_relationship_kwargs={"foreign_keys": "[TrainSchedule.departure_station_id]"},
    )
    arrival_station: "Station" = Relationship(
        back_populates="arrival_schedules",
        sa_relationship_kwargs={"foreign_keys": "[TrainSchedule.arrival_station_id]"},
    )
    reservations: list["Reservation"] = Relationship(back_populates="schedule")
