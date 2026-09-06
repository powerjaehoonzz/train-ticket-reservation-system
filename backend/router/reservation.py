from fastapi import APIRouter, Depends, status

from core.dependencies import get_reservation_service
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
    user_id: int,
    reservation_service: ReservationService = Depends(get_reservation_service),
) -> ReservationRead:
    return await reservation_service.create(reservation_in, user_id)
