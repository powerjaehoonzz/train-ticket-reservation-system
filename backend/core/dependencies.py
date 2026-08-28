from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from core.database import get_session
from repository.station import StationRepository
from service.station import StationService


def get_station_repository(
    session: AsyncSession = Depends(get_session),
) -> StationRepository:
    return StationRepository(session)


def get_station_service(
    session: AsyncSession = Depends(get_session),
    station_repository: StationRepository = Depends(get_station_repository),
) -> StationService:
    return StationService(session, station_repository)
