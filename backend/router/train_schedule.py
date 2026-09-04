from fastapi import APIRouter, Depends, status

from core.dependencies import get_train_schedule_service
from service.train_schedule import TrainScheduleService
from schemas.train_schedule import (
    TrainScheduleCreate,
    TrainScheduleRead,
    TrainScheduleSearch,
    TrainScheduleSearchRead,
)

router = APIRouter(
    prefix="/train_schedules",
    tags=["TrainSchedule"],
)


@router.post(
    "",
    response_model=TrainScheduleRead,
    status_code=status.HTTP_201_CREATED,
)
async def create_train_schedule(
    train_schedule_in: TrainScheduleCreate,
    train_schedule_service: TrainScheduleService = Depends(get_train_schedule_service),
) -> TrainScheduleRead:
    return await train_schedule_service.create(train_schedule_in)


@router.get("/search", response_model=list[TrainScheduleSearchRead])
async def search_train_schedules(
    train_schedule_search_in: TrainScheduleSearch = Depends(),
    train_schedule_service: TrainScheduleService = Depends(get_train_schedule_service),
) -> list[TrainScheduleSearchRead]:
    return await train_schedule_service.search(train_schedule_search_in)
