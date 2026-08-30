from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from enums.train import TrainType
from models.train import Train


class TrainRepository:
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def create(self, train: Train) -> Train:
        self._session.add(train)

        await self._session.flush()
        await self._session.refresh(train)

        return train

    async def get_by_type_and_number(
        self, train_type: TrainType, train_number: str
    ) -> Train | None:
        stmt = select(Train).where(
            Train.train_type == train_type,
            Train.train_number == train_number,
        )

        result = await self._session.execute(stmt)

        return result.scalar_one_or_none()
