from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field

from enums.reservation import ReservationStatus


class ReservationCreate(BaseModel):
    schedule_id: int = Field(gt=0)
    seat_id: int = Field(gt=0)


class ReservationRead(BaseModel):
    id: int
    user_id: int
    schedule_id: int
    seat_id: int
    status: ReservationStatus
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)
