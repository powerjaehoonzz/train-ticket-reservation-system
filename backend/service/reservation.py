from datetime import datetime, timedelta, timezone

from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import IntegrityError

from enums.reservation import ReservationStatus
from repository.seat import SeatRepository
from repository.train_schedule import TrainScheduleRepository
from models.reservation import Reservation
from schemas.reservation import ReservationCreate
from repository.reservation import ReservationRepository


class ReservationService:
    def __init__(
        self,
        session: AsyncSession,
        reservation_repository: ReservationRepository,
        train_schedule_repository: TrainScheduleRepository,
        seat_repository: SeatRepository,
    ) -> None:
        self._session = session
        self._reservation_repository = reservation_repository
        self._train_schedule_repository = train_schedule_repository
        self._seat_repository = seat_repository

    async def create(
        self,
        user_id: int,
        reservation_in: ReservationCreate,
    ) -> Reservation:
        schedule = await self._train_schedule_repository.get_by_id(
            reservation_in.schedule_id
        )

        if schedule is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="존재하지 않는 운행입니다.",
            )

        seat = await self._seat_repository.get_by_id(reservation_in.seat_id)

        if seat is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="존재하지 않는 좌석입니다.",
            )

        if seat.train_id != schedule.train_id:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="좌석이 운행과 일치하지 않습니다.",
            )

        if schedule.departure_time <= datetime.now(timezone.utc):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="이미 출발한 운행의 예약은 불가능합니다.",
            )

        existing_reservation = (
            await self._reservation_repository.find_active_by_schedule_and_seat(
                reservation_in.schedule_id, reservation_in.seat_id
            )
        )

        if existing_reservation is not None:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="이미 예약된 좌석입니다.",
            )

        reservation = Reservation(
            user_id=user_id,
            schedule_id=reservation_in.schedule_id,
            seat_id=reservation_in.seat_id,
        )

        try:
            await self._reservation_repository.create(reservation)
            await self._session.commit()
        except IntegrityError:
            await self._session.rollback()
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="이미 예약된 좌석입니다.",
            )
        except Exception:
            await self._session.rollback()
            raise

        return reservation

    async def get_by_user_id(self, user_id: int) -> list[Reservation]:
        return await self._reservation_repository.get_by_user_id(user_id)

    async def cancel(self, user_id: int, reservation_id: int) -> Reservation:
        reservation = await self._reservation_repository.get_by_id(reservation_id)

        if reservation is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="존재하지 않는 예약입니다.",
            )

        if user_id != reservation.user_id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="예약은 본인만 취소할 수 있습니다.",
            )

        if reservation.status == ReservationStatus.CANCELLED:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="이미 취소된 예약입니다.",
            )

        cancel_deadline = reservation.schedule.departure_time - timedelta(minutes=5)

        if datetime.now(timezone.utc) > cancel_deadline:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="출발 5분전까지만 예약을 취소할 수 있습니다.",
            )

        try:
            await self._reservation_repository.cancel(reservation)
            await self._session.commit()
        except Exception:
            await self._session.rollback()
            raise

        return reservation
