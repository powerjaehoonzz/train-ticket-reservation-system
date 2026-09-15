from typing import TypedDict

from models.seat import Seat
from models.train import Train
from models.train_schedule import TrainSchedule


class ReservationData(TypedDict):
    train: Train
    seat: Seat
    schedule: TrainSchedule
