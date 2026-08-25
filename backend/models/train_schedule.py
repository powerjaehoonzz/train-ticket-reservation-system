from datetime import datetime

from sqlalchemy import Column, DateTime, func
from sqlmodel import Field, SQLModel


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
