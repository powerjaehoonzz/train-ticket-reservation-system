from datetime import datetime

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from models.train_schedule import TrainSchedule


class TrainScheduleRepository:
    def __init__(
        self,
        session: AsyncSession,
    ) -> None:
        self._session = session

    async def create(self, train_schedule: TrainSchedule) -> TrainSchedule:
        self._session.add(train_schedule)

        await self._session.flush()
        await self._session.refresh(train_schedule)

        return train_schedule

    async def has_schedule_conflict(
        self,
        train_id: int,
        departure_time: datetime,
        arrival_time: datetime,
        exclude_schedule_id: int | None = None,
    ) -> bool:
        stmt = select(TrainSchedule).where(
            TrainSchedule.train_id == train_id,
            TrainSchedule.departure_time < arrival_time,
            TrainSchedule.arrival_time > departure_time,
        )

        if exclude_schedule_id is not None:
            stmt = stmt.where(TrainSchedule.id != exclude_schedule_id)

        result = await self._session.execute(stmt)

        return result.scalar_one_or_none() is not None
