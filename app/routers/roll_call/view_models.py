from enum import Enum

from pydantic import BaseModel

from datetime import datetime, date

from app.core.models.organization import Department, Organization, Employee
from app.core.models.organization.position import Position
from app.core.models.roll_call.roll_call import RollCall
from app.routers.auth.view_models import CurrentUserViewModel


class OrganizationResponse(BaseModel):
    name: str
    legal_name: str
    legal_name_prefix: str
    location_lat: float | None = None
    location_lng: float | None = None
    id: int
    created_at: datetime
    updated_at: datetime

    @staticmethod
    def from_model(model: Organization):
        response = OrganizationResponse(
            id=model.id,
            name=model.name,
            legal_name=model.legal_name,
            legal_name_prefix=model.legal_name_prefix,
            location_lat=model.location_lat,
            location_lng=model.location_lng,
            created_at=model.created_at,
            updated_at=model.updated_at,
        )
        return response


class PositionViewModel(BaseModel):
    id: int
    name: str

    @staticmethod
    def from_model(model: Position):
        return PositionViewModel(
            id=model.id,
            name=model.name
        )


class DepartmentResponse(BaseModel):
    id: int
    name: str
    organization: object | None = None

    created_at: datetime
    updated_at: datetime

    @staticmethod
    def from_model(model: Department):
        response = DepartmentResponse(
            id=model.id,
            name=model.name,
            created_at=model.created_at,
            updated_at=model.updated_at
        )
        if 'organization' in model.__dict__:
            response.organization = OrganizationResponse.from_model(model.organization)

        return response


class EmployeeResponse(BaseModel):
    id: int
    phone: str
    user: CurrentUserViewModel | None = None
    department: DepartmentResponse | None = None
    position: PositionViewModel | None = None

    created_at: datetime
    updated_at: datetime

    @staticmethod
    def from_model(model: Employee):
        response = EmployeeResponse(
            id=model.id,
            phone=model.phone,
            created_at=model.created_at,
            updated_at=model.updated_at
        )
        if 'department' in model.__dict__:
            response.department = DepartmentResponse.from_model(model.department)
        if 'user' in model.__dict__:
            response.user = CurrentUserViewModel.from_model(model.user)
        if 'position' in model.__dict__ and model.position:
            response.position = PositionViewModel.from_model(model.position)
        return response


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
    employee: EmployeeResponse | None = None
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
        if 'employee' in roll_call.__dict__:
            response.employee = EmployeeResponse.from_model(roll_call.employee)

        return response
