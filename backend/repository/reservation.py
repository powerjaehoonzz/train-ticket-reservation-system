from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from enums.reservation import ReservationStatus
from models.reservation import Reservation


class ReservationRepository:
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def create(self, reservation: Reservation) -> Reservation:
        self._session.add(reservation)

        await self._session.flush()
        await self._session.refresh(reservation)

        return reservation

    async def find_active_by_schedule_and_seat(
        self, schedule_id: int, seat_id: int
    ) -> Reservation | None:
        stmt = select(Reservation).where(
            Reservation.schedule_id == schedule_id,
            Reservation.seat_id == seat_id,
            Reservation.status != ReservationStatus.CANCELLED,
        )

        result = await self._session.execute(stmt)

        return result.scalar_one_or_none()
