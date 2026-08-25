from datetime import datetime

from sqlalchemy import Column, DateTime, func
from sqlmodel import Field, SQLModel

from enums.train import TrainType


class Train(SQLModel, table=True):
    __tablename__ = "trains"

    id: int | None = Field(default=None, primary_key=True)
    train_type: TrainType = Field(nullable=False)
    train_number: str = Field(min_length=1, max_length=10, nullable=False)
    capacity: int = Field(gt=0, multiple_of=2, nullable=False)
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
