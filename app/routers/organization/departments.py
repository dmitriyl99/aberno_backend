from typing import Annotated, List

from fastapi import APIRouter, Depends, status

from app.use_cases.organization.department import (GetDepartmentsUseCase)
from .view_models import DepartmentResponse

router = APIRouter(prefix="/departments", tags=['admin-departments'])


@router.get('/', status_code=status.HTTP_200_OK, response_model=List[DepartmentResponse])
async def get_departments(
        get_departments_use_case: Annotated[GetDepartmentsUseCase, Depends(GetDepartmentsUseCase)],
        organization_id: int | None = None,
        search: str | None = None,
):
    departments = get_departments_use_case.execute(search, organization_id)

    return list(
        map(
            lambda department: DepartmentResponse.from_model(department), departments
        )
    )