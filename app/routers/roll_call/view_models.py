from pydantic import BaseModel
from enum import Enum

from datetime import datetime, date


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


class RollCallSickLeaveResponse(BaseModel):
    id: int
    date_from: date
    date_to: date
    note: str | None = None


class RollCallResponse(BaseModel):
    id: int
    status: RollCallStatusEnum
    note: str | None = None
    location: RollCallLocation | None = None
    sick_leave: RollCallSickLeaveResponse | None = None
    created_at: datetime
    updated_at: datetime



