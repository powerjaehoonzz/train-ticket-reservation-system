from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jwt.exceptions import InvalidTokenError
from sqlalchemy.ext.asyncio import AsyncSession

from core.jwt import jwt_service
from models.user import User
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

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")


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
    return ReservationRepository(session)


def get_reservation_service(
    session: AsyncSession = Depends(get_session),
    reservation_repository=Depends(get_reservation_repository),
    train_schedule_repository=Depends(get_train_schedule_repository),
    seat_repository=Depends(get_seat_repository),
) -> ReservationService:
    return ReservationService(
        session, reservation_repository, train_schedule_repository, seat_repository
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


async def get_current_user(
    token: str = Depends(oauth2_scheme),
    user_repository: UserRepository = Depends(get_user_repository),
) -> User:
    try:
        payload = jwt_service.decode_and_verify(token, expected_type="access")
        user_id = int(payload["sub"])
    except (InvalidTokenError, KeyError, TypeError, ValueError):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="유효하지 않은 엑세스 토큰입니다.",
            headers={"WWW-Authenticate": "Bearer"},
        )

    user = await user_repository.get_by_id(user_id)

    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="사용자를 찾을 수 없습니다.",
            headers={"WWW-Authenticate": "Bearer"},
        )

    return user
