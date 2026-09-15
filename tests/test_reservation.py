import asyncio
from datetime import datetime, timedelta, timezone

from httpx import AsyncClient

import pytest_asyncio
from sqlalchemy.ext.asyncio import AsyncSession

from enums.seat import SeatClass
from enums.station import Region
from enums.train import TrainType
from models.seat import Seat
from models.station import Station
from models.train import Train
from models.train_schedule import TrainSchedule
from tests.types import ReservationData


@pytest_asyncio.fixture
async def reservation_data(test_session: AsyncSession) -> ReservationData:
    departure_station = Station(
        name="서울역",
        code="SEO",
        city="서울",
        region=Region.CAPITAL,
    )

    arrival_station = Station(
        name="부산역",
        code="BUS",
        city="부산",
        region=Region.YEONGNAM,
    )

    train = Train(
        train_type=TrainType.KTX,
        train_number="100",
        capacity=40,
    )

    seat = Seat(
        train=train,
        seat_number="1A",
        seat_class=SeatClass.STANDARD,
    )

    schedule = TrainSchedule(
        train=train,
        departure_station=departure_station,
        arrival_station=arrival_station,
        departure_time=datetime.now(timezone.utc) + timedelta(hours=1),
        arrival_time=datetime.now(timezone.utc) + timedelta(hours=4),
    )

    test_session.add_all(
        [
            departure_station,
            arrival_station,
            train,
            seat,
            schedule,
        ]
    )

    await test_session.commit()

    await test_session.refresh(train)
    await test_session.refresh(seat)
    await test_session.refresh(schedule)

    return {
        "train": train,
        "seat": seat,
        "schedule": schedule,
    }


async def test_create_reservation_success(
    client: AsyncClient,
    reservation_data: ReservationData,
):
    response = await client.post(
        "/reservations",
        json={
            "schedule_id": reservation_data["schedule"].id,
            "seat_id": reservation_data["seat"].id,
        },
    )

    assert response.status_code == 201

    data = response.json()

    assert data["schedule_id"] == reservation_data["schedule"].id
    assert data["seat_id"] == reservation_data["seat"].id
    assert data["status"] == "결제대기"


async def test_create_reservation_duplicate(
    client: AsyncClient,
    reservation_data: ReservationData,
):
    reservation_payload = {
        "schedule_id": reservation_data["schedule"].id,
        "seat_id": reservation_data["seat"].id,
    }

    first_response = await client.post("/reservations", json=reservation_payload)

    assert first_response.status_code == 201

    second_response = await client.post("/reservations", json=reservation_payload)

    assert second_response.status_code == 409
    assert second_response.json()["detail"] == "이미 예약된 좌석입니다."


async def test_create_reservation_concurrency(
    client: AsyncClient, reservation_data: ReservationData
):
    payload = {
        "schedule_id": reservation_data["schedule"].id,
        "seat_id": reservation_data["seat"].id,
    }

    responses = await asyncio.gather(
        *(client.post("/reservations", json=payload) for _ in range(10))
    )

    status_codes = [response.status_code for response in responses]

    assert status_codes.count(201) == 1
    assert status_codes.count(409) == 9
