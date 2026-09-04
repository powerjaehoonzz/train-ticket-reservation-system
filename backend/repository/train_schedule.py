from datetime import date, datetime, time, timedelta

from sqlalchemy import and_, func, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import aliased

from enums.reservation import ReservationStatus
from models.reservation import Reservation
from models.station import Station
from models.train import Train
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

    async def get_by_id(self, train_schedule_id: int) -> TrainSchedule | None:
        return await self._session.get(TrainSchedule, train_schedule_id)

    async def get_all(self) -> list[TrainSchedule]:
        stmt = select(TrainSchedule).order_by(TrainSchedule.id)
        result = await self._session.execute(stmt)

        return result.scalars().all()

    async def search(
        self,
        departure_station_id: int,
        arrival_station_id: int,
        departure_date: date,
    ) -> list[tuple[TrainSchedule, Train, Station, Station, int]]:
        DepartureStation = aliased(Station)
        ArrivalStation = aliased(Station)

        reserved_seat_count = func.count(Reservation.id)
        remaining_seats = (Train.capacity - reserved_seat_count).label(
            "remaining_seats"
        )

        start_datetime = datetime.combine(departure_date, time.min)
        end_datetime = start_datetime + timedelta(days=1)

        stmt = (
            select(
                TrainSchedule,
                Train,
                DepartureStation,
                ArrivalStation,
                remaining_seats,
            )
            .join(
                Train,
                Train.id == TrainSchedule.train_id,
            )
            .join(
                DepartureStation,
                DepartureStation.id == TrainSchedule.departure_station_id,
            )
            .join(
                ArrivalStation,
                ArrivalStation.id == TrainSchedule.arrival_station_id,
            )
            .outerjoin(
                Reservation,
                and_(
                    Reservation.schedule_id == TrainSchedule.id,
                    Reservation.status != ReservationStatus.CANCELLED,
                ),
            )
            .where(
                TrainSchedule.departure_station_id == departure_station_id,
                TrainSchedule.arrival_station_id == arrival_station_id,
                TrainSchedule.departure_time >= start_datetime,
                TrainSchedule.departure_time < end_datetime,
            )
            .group_by(
                TrainSchedule.id,
                Train.id,
                DepartureStation.id,
                ArrivalStation.id,
                Train.capacity,
            )
            .order_by(TrainSchedule.departure_time)
        )

        result = await self._session.execute(stmt)

        return result.tuples().all()
