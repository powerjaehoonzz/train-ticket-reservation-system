from fastapi import APIRouter, Depends, status

from core.dependencies import get_train_service
from service.train import TrainService
from schemas.train import TrainCreate, TrainRead

router = APIRouter(
    prefix="/trains",
    tags=["Train"],
)


@router.post(
    "",
    response_model=TrainRead,
    status_code=status.HTTP_201_CREATED,
)
async def create_train(
    train_in: TrainCreate,
    train_service: TrainService = Depends(get_train_service),
) -> TrainRead:
    return await train_service.create(train_in)
