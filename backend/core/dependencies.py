from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from service.auth import AuthService
from repository.user import UserRepository
from repository.reservation import ReservationRepository
from service.reservation import ReservationService
from service.train_schedule import TrainScheduleService
from repository.train_schedule import TrainScheduleRepository
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


def get_train_schedule_repository(
    session: AsyncSession = Depends(get_session),
) -> TrainScheduleRepository:
    return TrainScheduleRepository(session)


def get_train_schedule_service(
    session: AsyncSession = Depends(get_session),
    train_schedule_repository: TrainScheduleRepository = Depends(
        get_train_schedule_repository
    ),
    train_repository: TrainRepository = Depends(get_train_repository),
    station_repository: StationRepository = Depends(get_station_repository),
) -> TrainScheduleService:
    return TrainScheduleService(
        session, train_schedule_repository, train_repository, station_repository
    )


def get_reservation_repository(
    session: AsyncSession = Depends(get_session),
) -> ReservationRepository:
    return get_reservation_repository(session)


def get_reservation_service(
    session: AsyncSession = Depends(get_session),
    reservation_repository=Depends(get_reservation_repository),
    train_repository=Depends(get_train_repository),
    seat_repository=Depends(get_seat_repository),
) -> ReservationService:
    return ReservationService(
        session, reservation_repository, train_repository, seat_repository
    )


def get_user_repository(
    session: AsyncSession = Depends(get_session),
) -> UserRepository:
    return UserRepository(session)


def get_auth_service(
    session: AsyncSession = Depends(get_session),
    user_repository: UserRepository = Depends(get_user_repository),
) -> AuthService:
    return AuthService(session, user_repository)
