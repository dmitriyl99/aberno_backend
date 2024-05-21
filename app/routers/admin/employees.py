import datetime
from datetime import date, timedelta
from typing import Annotated
import calendar

from fastapi import APIRouter, Depends, status, HTTPException

from app.use_cases.organization.employee import (
    GetEmployeesUseCase,
    GetEmployeeByIdUseCase,
    UpdateEmployeeUseCase,
    DeleteEmployeeUseCase,
    CreateEmployeeUseCase,
    GetRolesUseCase,
    RemoveEmployeeRoleUseCase,
    ReactivateEmployeeUseCase
)
from app.core.facades.auth import Auth

from .view_models import CreateEmployeeViewModel, EmployeeResponse, ChangeRoleViewModel
from ..roll_call.view_models import RollCallStatusEnum
from ...core.models.roll_call.roll_call import RollCall
from ...use_cases.organization.employee.change_employee_role_use_case import ChangeEmployeeRoleUseCase
from ...use_cases.roll_call.get_roll_call_history_user_case import GetRollCallHistoryUseCase

router = APIRouter(prefix='/employees', tags=['admin-employees'])


@router.get("/", status_code=status.HTTP_200_OK)
async def get_employees(
        get_employees_use_case: Annotated[GetEmployeesUseCase, Depends(GetEmployeesUseCase)],
        search: str | None = None,
        department_id: int | None = None,
        page: int = 1,
        per_page: int = 10
):
    employees, count = get_employees_use_case.execute(Auth.get_current_user(), search, department_id, page, per_page)

    return {
        'count': count,
        'data': list(
            map(lambda employee: EmployeeResponse.from_model(employee), employees)
        )
    }


@router.get('/roles', status_code=status.HTTP_200_OK)
async def get_roles(
        get_roles_use_case: Annotated[GetRolesUseCase, Depends(GetRolesUseCase)]
):
    return get_roles_use_case.execute()


@router.get("/{employee_id}")
async def get_employee_by_id(
        get_employee_by_id_use_case: Annotated[GetEmployeeByIdUseCase, Depends(GetEmployeeByIdUseCase)],
        employee_id: int
):
    employee = get_employee_by_id_use_case.execute(Auth.get_current_user(), employee_id)
    if not employee:
        raise HTTPException(status_code=404, detail="Employee not found")

    return EmployeeResponse.from_model(employee)


@router.post("/{employee_id}/role", status_code=status.HTTP_204_NO_CONTENT)
async def change_role(
        change_employee_role_use_case: Annotated[ChangeEmployeeRoleUseCase, Depends(ChangeEmployeeRoleUseCase)],
        employee_id: int,
        data: ChangeRoleViewModel
):
    change_employee_role_use_case.execute(employee_id, data.role_id)


@router.delete("/{employee_id}/role", status_code=status.HTTP_204_NO_CONTENT)
async def delete_role(
        remove_employee_role_use_case: Annotated[RemoveEmployeeRoleUseCase, Depends(RemoveEmployeeRoleUseCase)],
        employee_id: int,
        data: ChangeRoleViewModel
):
    remove_employee_role_use_case.execute(employee_id, data.role_id)


@router.get("/{employee_id}/roll-call-history")
async def get_employee_roll_call_history(
        get_employee_by_id_use_case: Annotated[GetEmployeeByIdUseCase, Depends(GetEmployeeByIdUseCase)],
        get_roll_call_history_use_case: Annotated[GetRollCallHistoryUseCase, Depends(GetRollCallHistoryUseCase)],
        employee_id: int,
        filter_date: date | None = None,
):
    if not filter_date:
        filter_date = date.today()
    employee = get_employee_by_id_use_case.execute(Auth.get_current_user(), employee_id)
    if not employee:
        raise HTTPException(status_code=404, detail="Employee not found")
    roll_call_history = get_roll_call_history_use_case.execute(employee.user, None, None)

    start_date = filter_date.replace(day=1)
    end_date = filter_date.replace(day=calendar.monthrange(filter_date.year, filter_date.month)[1])
    result = {}
    current_date = start_date
    while current_date <= end_date:
        filtered_roll_calls = list(
            filter(
                lambda r: r.created_at.date() == current_date, roll_call_history
            ))
        date_roll_call: RollCall | None = None
        if len(filtered_roll_calls) > 0:
            date_roll_call = filtered_roll_calls[0]
        result[current_date.strftime('%Y-%m-%d')] = {
            'status': None, 'note': None, 'on-work': None, 'leave-work': None, 'work-duration': None
        }
        if date_roll_call:
            on_work_time = None
            leave_work_time = None
            work_duration = None
            if date_roll_call.status == RollCallStatusEnum.ON_WORK:
                on_work_time = date_roll_call.created_at
                leave_work_roll_call = list(
                    filter(
                        lambda
                            rch: rch.created_at.date() == current_date and rch.status == RollCallStatusEnum.LEAVE_WORK,
                        roll_call_history
                    )
                )
                if len(leave_work_roll_call) > 0:
                    leave_work_time = leave_work_roll_call[0].created_at
            if date_roll_call.status == RollCallStatusEnum.LEAVE_WORK:
                leave_work_time = date_roll_call.created_at
                on_work_roll_call = list(
                    filter(
                        lambda rch: rch.created_at.date() == current_date and rch.status == RollCallStatusEnum.ON_WORK,
                        roll_call_history
                    )
                )
                if len(on_work_roll_call) > 0:
                    on_work_time = on_work_roll_call[0].created_at
            if on_work_time and leave_work_time:
                difference: datetime.timedelta = leave_work_time - on_work_time
                work_duration = round(difference.seconds / 60)

            result[current_date.strftime('%Y-%m-%d')] = {
                'status': date_roll_call.status,
                'note': date_roll_call.note,
                'on-work': on_work_time,
                'leave-work': leave_work_time,
                'work-duration': work_duration
            }
        current_date += timedelta(days=1)

    sickness_roll_calls = filter(
        lambda r: r.status == RollCallStatusEnum.SICK, roll_call_history
    )
    for roll_call in sickness_roll_calls:
        current_date = roll_call.sick_leave.date_from
        while current_date <= roll_call.sick_leave.date_to:
            current_date_str = current_date.strftime('%Y-%m-%d')
            if current_date_str in result:
                result[current_date_str] = {
                    'status': RollCallStatusEnum.SICK,
                    'note': roll_call.note,
                    'on-work': None,
                    'leave-work': None,
                    'work-duration': None
                }
            current_date += timedelta(days=1)

    return result


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


@router.put("/{employee_id}/reactivate", status_code=status.HTTP_204_NO_CONTENT)
async def reactivate_employee(
        employee_id: int,
        reactivate_employee_use_case: Annotated[ReactivateEmployeeUseCase, Depends(ReactivateEmployeeUseCase)]
):
    reactivate_employee_use_case.execute(employee_id)


@router.delete("/{employee_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_employee(
        employee_id: int,
        delete_employee_use_case: Annotated[DeleteEmployeeUseCase, Depends(DeleteEmployeeUseCase)]
):
    result = delete_employee_use_case.execute(Auth.get_current_user(), employee_id)
    if not result:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Employee not found")
