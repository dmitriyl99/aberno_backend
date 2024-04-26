from typing import Annotated, List

from fastapi import APIRouter, Depends, status, HTTPException


from app.use_cases.organization.employee import (
    GetEmployeesUseCase, GetEmployeeByIdUseCase, UpdateEmployeeUseCase, DeleteEmployeeUseCase, CreateEmployeeUseCase)
from app.core.facades.auth import Auth


from .view_models import CreateEmployeeViewModel, EmployeeResponse
from ...core.models.organization import Employee

router = APIRouter(prefix='/employees', tags=['admin-employees'])


@router.get("/", status_code=status.HTTP_200_OK)
async def get_employees(
        get_employees_use_case: Annotated[GetEmployeesUseCase, Depends(GetEmployeesUseCase)],
        search: str | None = None,
        department_id: int | None = None,
):
    employees = get_employees_use_case.execute(Auth.get_current_user(), search, department_id)

    return list(
        map(lambda employee: EmployeeResponse.from_model(employee), employees)
    )


@router.get("/{employee_id}")
async def get_employee_by_id(
        get_employee_by_id_use_case: Annotated[GetEmployeeByIdUseCase, Depends(GetEmployeeByIdUseCase)],
        employee_id: int
):
    employee = get_employee_by_id_use_case.execute(Auth.get_current_user(), employee_id)
    if not employee:
        raise HTTPException(status_code=404, detail="Employee not found")

    return EmployeeResponse.from_model(employee)


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=EmployeeResponse)
async def create_employee(
        data: CreateEmployeeViewModel,
        create_employee_use_case: Annotated[CreateEmployeeUseCase, Depends(CreateEmployeeUseCase)]
):
    employee = create_employee_use_case.execute(Auth.get_current_user(), data)

    return EmployeeResponse.from_model(employee)


@router.put("/{employee_id}", response_model=EmployeeResponse)
async def update_employee(
        employee_id: int,
        data: CreateEmployeeViewModel,
        update_employee_use_case: Annotated[UpdateEmployeeUseCase, Depends(UpdateEmployeeUseCase)]
):
    employee = update_employee_use_case.execute(Auth.get_current_user(), employee_id, data)
    if not employee:
        raise HTTPException(status_code=404, detail="Employee not found")

    return EmployeeResponse.from_model(employee)


@router.delete("/{employee_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_employee(
        employee_id: int,
        delete_employee_use_case: Annotated[DeleteEmployeeUseCase, Depends(DeleteEmployeeUseCase)]
):
    result = delete_employee_use_case.execute(Auth.get_current_user(), employee_id)
    if not result:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Employee not found")
