from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from models.station import Station


class StationRepository:
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def create(self, station: Station) -> Station:
        self._session.add(station)

        await self._session.flush()
        await self._session.refresh(station)

        return station

    async def get_by_name(self, station_name: str) -> Station | None:
        stmt = select(Station).where(Station.name == station_name)
        result = await self._session.execute(stmt)

        return result.scalar_one_or_none()

    async def get_by_code(self, station_code: str) -> Station | None:
        stmt = select(Station).where(Station.code == station_code)
        result = await self._session.execute(stmt)

        return result.scalar_one_or_none()

    async def get_all(self) -> list[Station]:
        stmt = select(Station).order_by(Station.id)
        result = await self._session.execute(stmt)

        return result.scalars().all()

    async def get_by_id(self, station_id: int) -> Station | None:
        return await self._session.get(Station, station_id)
