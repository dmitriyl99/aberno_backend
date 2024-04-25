from datetime import datetime
from typing import List, Any

from pydantic import BaseModel
from sqlalchemy import inspect

from app.core.models.organization import Organization, Department


class CreateOrganizationViewModel(BaseModel):
    name: str
    legal_name: str
    legal_name_prefix: str
    location_lat: float | None = None
    location_lng: float | None = None


class CreateDepartmentViewModel(BaseModel):
    name: str
    organization_id: int


class EmployeeResponse(BaseModel):
    id: int
    name: str


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


class OrganizationResponse(CreateOrganizationViewModel):
    id: int
    created_at: datetime
    updated_at: datetime

    departments: List[DepartmentResponse] | None = None

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
        return response
