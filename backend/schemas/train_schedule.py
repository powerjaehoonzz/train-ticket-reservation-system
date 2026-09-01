from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field


class TrainScheduleCreate(BaseModel):
    train_id: int = Field(gt=0)
    departure_station_id: int = Field(gt=0)
    arrival_station_id: int = Field(gt=0)
    departure_time: datetime
    arrival_time: datetime


class TrainScheduleRead(BaseModel):
    id: int
    train_id: int
    departure_station_id: int
    arrival_station_id: int
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)
