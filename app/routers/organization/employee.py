from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status

from app.core.facades.auth import Auth
from app.routers.admin.view_models import EmployeeResponse
from app.tasks.organization.get_current_employee_task import GetCurrentEmployeeTask
from app.dependencies import verify_authenticated_user
from app.use_cases.organization.employee import GetEmployeesUseCase

router = APIRouter(prefix='/employee', dependencies=[Depends(verify_authenticated_user)])


@router.get("/", status_code=status.HTTP_200_OK)
async def get_employees(
        get_employees_use_case: Annotated[GetEmployeesUseCase, Depends(GetEmployeesUseCase)],
        search: str | None = None,
        department_id: int | None = None,
        position_id: int | None = None,
        status: str | None = None,
        page: int = 1,
        per_page: int = 10
):
    employees, count = get_employees_use_case.execute(
        Auth.get_current_user(),
        search,
        department_id,
        position_id,
        status,
        page,
        per_page,
        ['Employee', 'Admin', 'Super Admin']
    )

    return {
        'count': count,
        'data': list(
            map(lambda employee: EmployeeResponse.from_model(employee), employees)
        )
    }


@router.get('/current/')
async def current_employee(
        get_current_employee_task: Annotated[GetCurrentEmployeeTask, Depends(GetCurrentEmployeeTask)]
):
    current_user = Auth.get_current_user()
    current_employee = get_current_employee_task.run(current_user)
    if current_employee is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='Employee not found'
        )
    return current_employee

