from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from models.seat import Seat
from enums.seat import SeatClass
from models.train import Train
from schemas.train import TrainCreate
from repository.seat import SeatRepository
from repository.train import TrainRepository


class TrainService:
    def __init__(
        self,
        session: AsyncSession,
        train_repository: TrainRepository,
        seat_repository: SeatRepository,
    ) -> None:
        self._session = session
        self._train_repository = train_repository
        self._seat_repository = seat_repository

    async def create(self, train_in: TrainCreate) -> Train:
        existing_train = await self._train_repository.get_by_type_and_number(
            train_in.train_type, train_in.train_number
        )

        if existing_train is not None:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="이미 존재하는 열차입니다.",
            )

        train = Train(
            train_type=train_in.train_type,
            train_number=train_in.train_number,
            capacity=40,
        )

        try:
            await self._train_repository.create(train)

            seats = []

            for row in range(1, 11):
                seat_class = SeatClass.FIRST if row <= 2 else SeatClass.STANDARD

                for column in ("A", "B", "C", "D"):
                    seats.append(
                        Seat(
                            train_id=train.id,
                            seat_number=f"{row}{column}",
                            seat_class=seat_class,
                        )
                    )

            await self._seat_repository.create_many(seats)
            await self._session.commit()

        except Exception:
            await self._session.rollback()
            raise

        return train
