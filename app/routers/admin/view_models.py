from datetime import datetime, date
from typing import List, Any

from pydantic import BaseModel

from app.core.models.organization import Organization, Department, Employee
from app.routers.auth.view_models import CurrentUserViewModel


class CreateOrganizationViewModel(BaseModel):
    name: str
    legal_name: str
    legal_name_prefix: str
    location_lat: float | None = None
    location_lng: float | None = None


class CreateDepartmentViewModel(BaseModel):
    name: str
    organization_id: int


class CreateEmployeeViewModel(BaseModel):
    name: str
    last_name: str
    username: str
    password: str | None = None
    password_confirmation: str | None = None

    position: str
    phone: str
    department_id: int

    role_id: int | None = None


class ChangeRoleViewModel(BaseModel):
    role_id: int


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


class CreatedByViewModel(BaseModel):
    id: int
    name: str
    last_name: str | None


class EmployeeResponse(BaseModel):
    id: int
    phone: str
    user: CurrentUserViewModel | None = None
    department: DepartmentResponse | None = None
    position: str | None = None
    created_by: CurrentUserViewModel | None = None

    created_at: datetime
    updated_at: datetime

    @staticmethod
    def from_model(model: Employee):
        response = EmployeeResponse(
            id=model.id,
            phone=model.phone,
            position=model.position,
            created_at=model.created_at,
            updated_at=model.updated_at
        )
        if 'department' in model.__dict__:
            response.department = DepartmentResponse.from_model(model.department)
        if 'user' in model.__dict__:
            response.user = CurrentUserViewModel.from_model(model.user)
        if 'created_by' in model.__dict__ and model.created_by is not None:
            response.created_by = CreatedByViewModel(
                id=model.created_by.id,
                name=model.created_by.name,
                last_name=model.created_by.last_name
            )
        return response


class OrganizationSettingsViewModel(BaseModel):
    roll_call_start_time: str | None = None
    roll_call_end_time: str | None = None


class OrganizationResponse(CreateOrganizationViewModel):
    id: int
    created_at: datetime
    updated_at: datetime

    departments: List[DepartmentResponse] | None = None
    settings: OrganizationSettingsViewModel | None = None

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
        if 'departments' in model.__dict__:
            response.departments = list(
                map(
                    lambda department: DepartmentResponse(
                        id=department.id,
                        name=department.name
                    ), model.departments
                )
            )
        if 'settings' in model.__dict__:
            response.settings = OrganizationSettingsResponse(
                roll_call_start_time=model.settings.roll_call_start_time,
                roll_call_end_time=model.settings.roll_call_end_time
            )
        return response
