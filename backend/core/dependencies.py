from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from repository.seat import SeatRepository
from service.train import TrainService
from repository.train import TrainRepository
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


def get_seat_repository(
    session: AsyncSession = Depends(get_session),
) -> SeatRepository:
    return SeatRepository(session)


def get_train_repository(
    session: AsyncSession = Depends(get_session),
) -> TrainRepository:
    return TrainRepository(session)


def get_train_service(
    session: AsyncSession = Depends(get_session),
    train_repository: TrainRepository = Depends(get_train_repository),
    seat_repository: SeatRepository = Depends(get_seat_repository),
) -> TrainService:
    return TrainService(session, train_repository, seat_repository)
