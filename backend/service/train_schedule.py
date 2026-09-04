from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from models.train_schedule import TrainSchedule
from schemas.train_schedule import (
    TrainScheduleCreate,
    TrainScheduleSearch,
    TrainScheduleSearchRead,
)
from repository.station import StationRepository
from repository.train import TrainRepository
from repository.train_schedule import TrainScheduleRepository


class TrainScheduleService:
    def __init__(
        self,
        session: AsyncSession,
        train_schedule_repository: TrainScheduleRepository,
        train_repository: TrainRepository,
        station_repository: StationRepository,
    ) -> None:
        self._session = session
        self._train_schedule_repository = train_schedule_repository
        self._train_repository = train_repository
        self._station_repository = station_repository

    async def create(self, train_schedule_in: TrainScheduleCreate) -> TrainSchedule:
        train = await self._train_repository.get_by_id(train_schedule_in.train_id)

        if train is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="존재하지 않는 열차입니다.",
            )

        departure_station = await self._station_repository.get_by_id(
            train_schedule_in.departure_station_id
        )

        if departure_station is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="존재하지 않는 출발역입니다.",
            )

        arrival_station = await self._station_repository.get_by_id(
            train_schedule_in.arrival_station_id
        )

        if arrival_station is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="존재하지 않는 도착역입니다.",
            )

        if (
            train_schedule_in.departure_station_id
            == train_schedule_in.arrival_station_id
        ):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="출발역과 도착역은 같을 수 없습니다.",
            )

        if train_schedule_in.departure_time >= train_schedule_in.arrival_time:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="출발 시간은 도착 시간보다 빨라야 합니다.",
            )

        has_conflict = await self._train_schedule_repository.has_schedule_conflict(
            train_schedule_in.train_id,
            train_schedule_in.departure_time,
            train_schedule_in.arrival_time,
        )

        if has_conflict:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="해당 열차의 운행 시간이 기존 시간표와 겹칩니다.",
            )

        train_schedule = TrainSchedule(
            train_id=train_schedule_in.train_id,
            departure_station_id=train_schedule_in.departure_station_id,
            arrival_station_id=train_schedule_in.arrival_station_id,
            departure_time=train_schedule_in.departure_time,
            arrival_time=train_schedule_in.arrival_time,
        )

        try:
            await self._train_schedule_repository.create(train_schedule)
            await self._session.commit()

        except Exception:
            await self._session.rollback()
            raise

        return train_schedule

    async def search(
        self, train_schedule_in: TrainScheduleSearch
    ) -> list[TrainScheduleSearchRead]:
        schedules = await self._train_schedule_repository.search(
            train_schedule_in.departure_station_id,
            train_schedule_in.arrival_station_id,
            train_schedule_in.departure_date,
        )

        result = []

        for (
            train_schedule,
            train,
            departure_station,
            arrival_station,
            remaining_seats,
        ) in schedules:
            result.append(
                TrainScheduleSearchRead(
                    id=train_schedule.id,
                    train_id=train.id,
                    train_type=train.train_type,
                    train_number=train.train_number,
                    departure_station=departure_station.name,
                    arrival_station=arrival_station.name,
                    departure_time=train_schedule.departure_time,
                    arrival_time=train_schedule.arrival_time,
                    remaining_seats=remaining_seats,
                )
            )

        return result
