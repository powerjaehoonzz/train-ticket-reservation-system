from datetime import date, datetime

from pydantic import BaseModel, ConfigDict, Field

from enums.train import TrainType


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


class TrainScheduleSearch(BaseModel):
    departure_station_id: int = Field(gt=0)
    arrival_station_id: int = Field(gt=0)
    departure_date: date


class TrainScheduleSearchRead(BaseModel):
    id: int
    train_id: int
    train_type: TrainType
    train_number: str
    departure_station: str
    arrival_station: str
    departure_time: datetime
    arrival_time: datetime
    remaining_seats: int
