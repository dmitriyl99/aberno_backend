from datetime import datetime
from typing import List

from pydantic import BaseModel

from app.core.models.organization import Employee, Department
from app.core.models.tasks import Task, TaskStatusEnum, TaskPriorityEnum
from app.core.models.tasks.task import EmployeesTasks
from app.routers.admin.view_models import PositionViewModel
from app.routers.auth.view_models import CurrentUserViewModel


class DepartmentResponse(BaseModel):
    id: int
    name: str

    @staticmethod
    def from_model(department: Department):
        return DepartmentResponse(
            id=department.id,
            name=department.name
        )


class EmployeeResponse(BaseModel):
    id: int
    user: CurrentUserViewModel | None = None
    position: PositionViewModel | None = None

    @staticmethod
    def from_model(employee: Employee):
        response = EmployeeResponse(
            id=employee.id,
        )
        if 'user' in employee.__dict__:
            response.user = CurrentUserViewModel.from_model(employee.user)
        if 'position' in employee.__dict__:
            response.position = PositionViewModel.from_model(employee.position)

        return response


class EmployeeTaskResponse(BaseModel):
    employee: EmployeeResponse
    status: TaskStatusEnum
    viewed: bool
    viewed_at: datetime | None = None

    @staticmethod
    def from_model(employee_task: EmployeesTasks):
        response = EmployeeTaskResponse(
            status=employee_task.status,
            viewed=employee_task.viewed,
            viewed_at=employee_task.viewed_at,
        )
        if 'employee' in employee_task.__dict__ and employee_task.employee:
            response.employee = EmployeeResponse.from_model(employee_task.employee)
        return response


class TaskViewModel(BaseModel):
    title: str
    description: str | None
    priority: TaskPriorityEnum | None
    deadline: datetime | None

    department_id: int | None
    controller_id: int | None
    executors_ids: List[int] | None


class TaskExecutorViewModel(BaseModel):
    employee_id: int


class TaskStatusViewModel(BaseModel):
    status: TaskStatusEnum


class TaskResponse(TaskViewModel):
    id: int
    created_by_id: int
    status: TaskStatusEnum

    department: DepartmentResponse | None = None
    executors: List[EmployeeTaskResponse] | None = None
    created_by: EmployeeResponse | None = None
    controller: EmployeeResponse | None = None

    created_at: datetime
    updated_at: datetime

    @staticmethod
    def from_model(task: Task):
        response = TaskResponse(
            id=task.id,
            title=task.title,
            description=task.description,
            priority=task.priority,
            deadline=task.deadline,
            department_id=task.department_id,
            status=task.status,
            created_by_id=task.created_by_id,
            created_at=task.created_at,
            updated_at=task.updated_at,
            viewed=task.viewed or False,
            viewed_at=task.viewed_at
        )
        if 'department' in task.__dict__ and task.department:
            response.department = DepartmentResponse.from_model(task.department)

        if 'executors' in task.__dict__ and task.executors:
            response.executors = list(map(lambda e: EmployeeTaskResponse.from_model(e), task.executors))

        if 'created_by' in task.__dict__ and task.created_by:
            response.created_by = EmployeeResponse.from_model(task.created_by)

        if 'controller' in task.__dict__ and task.controller:
            response.controller = EmployeeResponse.from_model(task.controller)

        return response
