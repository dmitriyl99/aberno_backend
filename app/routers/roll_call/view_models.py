from enum import Enum

from pydantic import BaseModel

from datetime import datetime, date

from app.core.models.roll_call.roll_call import RollCall
# from app.routers.admin.view_models import EmployeeResponse


class RollCallStatusEnum(str, Enum):
    ON_WORK = 'ON_WORK'
    OFF_DAY = 'OFF_DAY'
    LATE = 'LATE',
    SICK = 'SICK'
    ABSENT = 'ABSENT'
    REASONED = 'REASONED'
    LEAVE_WORK = 'LEAVE_WORK'


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


class RollCallLeaveWorkResponse(BaseModel):
    leave_time: datetime
    leave_note: str | None = None
    leave_with_location: bool | None = None


class RollCallResponse(BaseModel):
    id: int
    status: RollCallStatusEnum
    note: str | None = None
    location: RollCallLocation | None = None
    sick_leave: RollCallSickLeaveResponse | None = None
    leave_work: RollCallLeaveWorkResponse | None = None
    # employee: EmployeeResponse | None = None
    created_at: datetime
    updated_at: datetime

    @staticmethod
    def from_model(roll_call: RollCall):
        response = RollCallResponse(
            id=roll_call.id,
            status=roll_call.status,
            note=roll_call.note,
            created_at=roll_call.created_at,
            updated_at=roll_call.updated_at
        )
        if 'sick_leave' in roll_call.__dict__:
            response.sick_leave = RollCallSickLeaveResponse(
                id=roll_call.sick_leave.id,
                date_from=roll_call.sick_leave.date_from,
                date_to=roll_call.sick_leave.date_to,
                note=roll_call.sick_leave.note
            ) if roll_call.sick_leave else None
        # if 'employee' in roll_call.__dict__:
        #     response.employee = EmployeeResponse.from_model(roll_call.employee)

        return response
