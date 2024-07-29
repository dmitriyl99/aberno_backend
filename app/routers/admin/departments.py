from typing import Annotated, List

from fastapi import APIRouter, Depends, status, HTTPException

from app.use_cases.organization.department import (CreateDepartmentUseCase, GetDepartmentByIdUseCase,
                                                   GetDepartmentsUseCase, UpdateDepartmentUseCase,
                                                   DeleteDepartmentUseCase, CreateDepartmentScheduleUseCase)
from .view_models import CreateDepartmentViewModel, DepartmentResponse, ScheduleDayViewModel

router = APIRouter(prefix="/departments", tags=['admin-departments'])


@router.get('/', status_code=status.HTTP_200_OK, response_model=List[DepartmentResponse])
async def get_departments(
        get_departments_use_case: Annotated[GetDepartmentsUseCase, Depends(GetDepartmentsUseCase)],
        organization_id: int | None = None,
        search: str | None = None,
        page: int = 1,
        per_page: int = 10
):
    count, departments = get_departments_use_case.execute(search, organization_id, page, per_page)

    return {
        'count': count,
        'data': list(
            map(
                lambda department: DepartmentResponse.from_model(department), departments
            )
        )
    }


@router.get('/{department_id}', response_model=DepartmentResponse)
async def get_department(
        department_id: int,
        get_department_by_id_use_case: Annotated[GetDepartmentByIdUseCase, Depends(GetDepartmentByIdUseCase)]
):
    department = get_department_by_id_use_case.execute(department_id)
    if not department:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='Department with id {} not found'.format(department_id)
        )

    return DepartmentResponse.from_model(department) \
 \
 \
@router.post('/{department_id}/schedule',
             status_code=status.HTTP_201_CREATED, response_model=List[ScheduleDayViewModel])
async def create_schedule(
        department_id: int,
        create_department_schedule_use_case: Annotated[
            CreateDepartmentScheduleUseCase, Depends(CreateDepartmentScheduleUseCase)],
        days: List[ScheduleDayViewModel]
):
    unique_days = set(map(lambda day: day.day.value, days))
    if len(unique_days) != 7:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail='The week is not full'
        )
    schedule = create_department_schedule_use_case.execute(department_id, days)

    return list(
        map(lambda day: ScheduleDayViewModel.from_model(day), schedule)
    )


@router.post('/', status_code=status.HTTP_201_CREATED, response_model=DepartmentResponse)
async def create_department(
        department: CreateDepartmentViewModel,
        create_department_use_case: Annotated[CreateDepartmentUseCase, Depends(CreateDepartmentUseCase)]
):
    department = create_department_use_case.execute(department)

    return DepartmentResponse.from_model(department)


@router.put('/{department_id}', status_code=status.HTTP_200_OK, response_model=DepartmentResponse)
async def update_department(
        department: CreateDepartmentViewModel,
        department_id: int,
        update_department_use_case: Annotated[UpdateDepartmentUseCase, Depends(UpdateDepartmentUseCase)]
):
    department = update_department_use_case.execute(department_id, department)
    if not department:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='Department with id {} not found'.format(department_id)
        )

    return DepartmentResponse.from_model(department)


@router.delete('/{department_id}', status_code=status.HTTP_204_NO_CONTENT)
async def delete_department(
        department_id: int,
        delete_department_use_case: Annotated[DeleteDepartmentUseCase, Depends(DeleteDepartmentUseCase)]
):
    result = delete_department_use_case.execute(department_id)
    if not result:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='Department with id {} not found'.format(department_id)
        )
