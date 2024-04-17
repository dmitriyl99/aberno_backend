from pydantic import BaseModel
from enum import Enum

from datetime import date


class RollCallStatusEnum(str, Enum):
    ON_WORK = 'ON_WORK'
    OFF_DAY = 'OFF_DAY'
    SICK = 'SICK'
    REASONED = 'REASONED'


class RollCallLocation(BaseModel):
    lat: float
    lng: float


class RollCallSickLeave(BaseModel):
    date_from: date
    date_to: date


class RollCallViewModel(BaseModel):
    status: RollCallStatusEnum
    note: str | None = None
    location: RollCallLocation | None = None
    sick_leave: RollCallSickLeave | None = None
