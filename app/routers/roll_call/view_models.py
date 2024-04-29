from pydantic import BaseModel
from enum import Enum

from datetime import datetime, date

from app.core.models.roll_call.roll_call import RollCall


class RollCallStatusEnum(str, Enum):
    ON_WORK = 'ON_WORK'
    OFF_DAY = 'OFF_DAY'
    LATE = 'LATE',
    SICK = 'SICK'
    ABSENT = 'ABSENT'
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

    @staticmethod
    def from_model(roll_call: RollCall):
        return RollCallResponse(
            id=roll_call.id,
            status=roll_call.status,
            note=roll_call.note,
            created_at=roll_call.created_at,
            updated_at=roll_call.updated_at,
            sick_leave=RollCallSickLeaveResponse(
                id=roll_call.sick_leave.id,
                date_from=roll_call.sick_leave.date_from,
                date_to=roll_call.sick_leave.date_to,
                note=roll_call.sick_leave.note
            ) if roll_call.sick_leave else None
        )
