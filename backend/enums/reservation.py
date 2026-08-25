from enum import StrEnum


class ReservationStatus(StrEnum):
    PENDING = "결제대기"
    CONFIRMED = "예약완료"
    CANCELLED = "취소됨"
