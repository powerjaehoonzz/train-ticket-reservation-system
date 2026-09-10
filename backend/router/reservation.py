from fastapi import APIRouter, Depends, status

from models.user import User
from core.dependencies import get_current_user, get_reservation_service
from service.reservation import ReservationService
from schemas.reservation import ReservationCreate, ReservationRead

router = APIRouter(prefix="/reservations", tags=["Reservation"])


@router.post(
    "",
    response_model=ReservationRead,
    status_code=status.HTTP_201_CREATED,
)
async def create_reservation(
    reservation_in: ReservationCreate,
    current_user: User = Depends(get_current_user),
    reservation_service: ReservationService = Depends(get_reservation_service),
) -> ReservationRead:
    return await reservation_service.create(current_user.id, reservation_in)
