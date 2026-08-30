from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field

from enums.train import TrainType


class TrainCreate(BaseModel):
    train_type: TrainType
    train_number: str = Field(min_length=1, max_length=10)

    model_config = ConfigDict(
        json_schema_extra={
            "examples": [
                {
                    "train_type": "KTX",
                    "train_number": "101",
                    "capacity": 40,
                }
            ]
        }
    )


class TrainRead(BaseModel):
    id: int
    train_type: TrainType
    train_number: str
    capacity: int
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)
