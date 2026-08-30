from sqlalchemy.ext.asyncio import AsyncSession

from models.seat import Seat


class SeatRepository:
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def create_many(self, seats: list[Seat]) -> list[Seat]:
        self._session.add_all(seats)

        await self._session.flush()

        return seats
