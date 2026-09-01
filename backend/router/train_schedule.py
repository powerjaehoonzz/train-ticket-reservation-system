from fastapi import APIRouter, Depends, status

from core.dependencies import get_train_schedule_service
from service.train_schedule import TrainScheduleService
from schemas.train_schedule import TrainScheduleCreate, TrainScheduleRead

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
