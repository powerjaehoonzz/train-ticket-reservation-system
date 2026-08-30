from fastapi import APIRouter, Depends, status

from core.dependencies import get_station_service
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


@router.get("", response_model=list[StationRead])
async def get_all_stations(
    station_service: StationService = Depends(get_station_service),
) -> list[StationRead]:
    return await station_service.get_all()


@router.get("/{station_id}", response_model=StationRead)
async def get_station_by_id(
    station_id: int, station_service: StationService = Depends(get_station_service)
) -> StationRead:
    return await station_service.get_by_id(station_id)
