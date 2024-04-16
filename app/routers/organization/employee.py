from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status

from app.core.facades.auth import Auth
from app.tasks.organization.get_current_employee_task import GetCurrentEmployeeTask
from app.dependencies import verify_authenticated_user


router = APIRouter(prefix='/employee', dependencies=[Depends(verify_authenticated_user)])


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

