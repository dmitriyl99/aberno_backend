from pydantic import BaseModel
from enum import Enum


class RollCallStatusEnum(str, Enum):
    ON_WORK = 'ON_WORK'
    OFF_DAY = 'OFF_DAY'
    SICK = 'SICK'
    REASONED = 'REASONED'


class RollCallLocation(BaseModel):
    lat: float
    lng: float


class RollCallViewModel(BaseModel):
    status: RollCallStatusEnum
    note: str | None = None
    location: RollCallLocation | None = None
