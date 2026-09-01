from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from models.station import Station
from schemas.station import StationCreate
from repository.station import StationRepository


class StationService:
    def __init__(
        self,
        session: AsyncSession,
        station_repository: StationRepository,
    ) -> None:
        self._session = session
        self._station_repository = station_repository

    async def create(self, station_in: StationCreate) -> Station:
        existing_station = await self._station_repository.get_by_name(station_in.name)

        if existing_station is not None:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="이미 존재하는 역입니다.",
            )

        existing_code = await self._station_repository.get_by_code(station_in.code)

        if existing_code is not None:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="이미 존재하는 역 코드입니다.",
            )

        station = Station(
            name=station_in.name,
            code=station_in.code,
            city=station_in.city,
            region=station_in.region,
        )

        try:
            await self._station_repository.create(station)
            await self._session.commit()

        except Exception:
            await self._session.rollback()
            raise

        return station

    async def get_all(self) -> list[Station]:
        return await self._station_repository.get_all()

    async def get_by_id(self, station_id: int) -> Station:
        station = await self._station_repository.get_by_id(station_id)

        if station is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="존재하지 않는 역입니다.",
            )

        return station
