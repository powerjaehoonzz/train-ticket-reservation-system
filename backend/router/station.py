from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from core.dependencies import get_station_service
from repository.station import StationRepository
from models.station import Station
from core.database import get_session
from schemas.station import StationCreate, StationRead
from service.station import StationService

router = APIRouter(
    prefix="/stations",
    tags=["Station"],
)


@router.post(
    "",
    response_model=StationRead,
    status_code=status.HTTP_201_CREATED,
)
async def create_station(
    station_in: StationCreate,
    station_service: StationService = Depends(get_station_service),
) -> StationRead:
    return await station_service.create(station_in)
