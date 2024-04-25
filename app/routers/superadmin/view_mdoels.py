from datetime import datetime
from typing import List

from pydantic import BaseModel
from sqlalchemy import inspect

from app.core.models.organization import Organization


class CreateOrganizationViewModel(BaseModel):
    name: str
    legal_name: str
    legal_name_prefix: str
    location_lat: float | None = None
    location_lng: float | None = None


class DepartmentResponse(BaseModel):
    id: int
    name: str


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
