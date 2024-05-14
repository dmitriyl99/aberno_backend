from datetime import date
from typing import List, Annotated

from fastapi import APIRouter, Depends, status as http_status

from app.dependencies import verify_authenticated_user
from .view_models import TaskResponse, TaskViewModel, TaskStatusViewModel
from app.use_cases.tasks import (
    GetTasksUseCase,
    UpdateTaskUseCase,
    ChangeTaskStatusUseCase,
    CreateTaskUseCase,
    GetTaskByIdUseCase
)
from app.core.facades.auth import Auth
from ...tasks.organization.get_current_employee_task import GetCurrentEmployeeTask

router = APIRouter(prefix='/tasks', tags=['tasks'], dependencies=[Depends(verify_authenticated_user)])


@router.get('/')
async def get_tasks(
        get_tasks_use_case: Annotated[GetTasksUseCase, Depends(GetTasksUseCase)],
        department_id: int | None = None,
        executor_id: int | None = None,
        status: str | None = None,
        priority: str | None = None,
        deadline: date | None = None,
        search: str | None = None,
        created_by_id: int | None = None,
        page: int = 1,
        per_page: int = 10
):
    tasks, count = get_tasks_use_case.execute(
        department_id, executor_id, status, priority, deadline, search, created_by_id, page, per_page
    )

    return {
        'count': count,
        'data': list(
            map(TaskResponse.from_model, tasks)
        )
    }


@router.get('/my-tasks')
async def get_my_tasks(
        get_tasks_use_case: Annotated[GetTasksUseCase, Depends(GetTasksUseCase)],
        get_current_employee_task: Annotated[GetCurrentEmployeeTask, Depends(GetCurrentEmployeeTask)],
        department_id: int | None = None,
        status: str | None = None,
        priority: str | None = None,
        deadline: date | None = None,
        search: str | None = None,
        created_by_id: int | None = None,
        page: int = 1,
        per_page: int = 10
):
    executor_id = get_current_employee_task.run(Auth.get_current_user()).id
    tasks, count = get_tasks_use_case.execute(
        department_id, executor_id, status, priority, deadline, search, created_by_id, page, per_page
    )

    return {
        'count': count,
        'data': list(
            map(TaskResponse.from_model, tasks)
        )
    }


@router.get('/created-by-me')
async def get_created_by_me(
        get_tasks_use_case: Annotated[GetTasksUseCase, Depends(GetTasksUseCase)],
        get_current_employee_task: Annotated[GetCurrentEmployeeTask, Depends(GetCurrentEmployeeTask)],
        department_id: int | None = None,
        executor_id: int | None = None,
        status: str | None = None,
        priority: str | None = None,
        deadline: date | None = None,
        search: str | None = None,
        page: int = 1,
        per_page: int = 10
):
    created_by_id = get_current_employee_task.run(Auth.get_current_user()).id
    tasks, count = get_tasks_use_case.execute(
        department_id, executor_id, status, priority, deadline, search, created_by_id, page, per_page
    )

    return {
        'count': count,
        'data': list(
            map(TaskResponse.from_model, tasks)
        )
    }


@router.get('/{task_id}', response_model=TaskResponse)
async def get_task(
        task_id: int,
        get_task_by_id_use_case: Annotated[GetTaskByIdUseCase, Depends(GetTaskByIdUseCase)]
):
    task = get_task_by_id_use_case.execute(task_id)
    return TaskResponse.from_model(task)


@router.post('/', response_model=TaskResponse, status_code=http_status.HTTP_201_CREATED)
async def create_task(
        dto: TaskViewModel,
        create_task_use_case: Annotated[CreateTaskUseCase, Depends(CreateTaskUseCase)]
):
    task = create_task_use_case.execute(dto)

    return TaskResponse.from_model(task)


@router.put('/{task_id}/status', response_model=TaskResponse)
async def update_task_status(
        task_id: int,
        status: TaskStatusViewModel,
        change_tasks_status_use_case: Annotated[ChangeTaskStatusUseCase, Depends(ChangeTaskStatusUseCase)]
):
    task = change_tasks_status_use_case.execute(task_id, status.status)
    return TaskResponse.from_model(task)


@router.put('/{task_id}', response_model=TaskResponse)
async def update_task(
        task_id: int,
        dto: TaskViewModel,
        update_task_use_case: Annotated[UpdateTaskUseCase, Depends(UpdateTaskUseCase)]
):
    task = update_task_use_case.execute(task_id, dto)

    return TaskResponse.from_model(task)
