from sqlalchemy.ext.asyncio import AsyncSession

from models.seat import Seat


class SeatRepository:
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def create_many(self, seats: list[Seat]) -> list[Seat]:
        self._session.add_all(seats)

        await self._session.flush()

        return seats

    async def get_by_id(self, seat_id: int) -> Seat | None:
        return await self._session.get(Seat, seat_id)
