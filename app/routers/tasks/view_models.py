from datetime import datetime
from typing import List

from pydantic import BaseModel

from app.core.models.organization import Employee, Department
from app.core.models.tasks import Task, TaskStatusEnum, TaskPriorityEnum
from app.core.models.tasks.task import EmployeesTasks, TaskComment
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
        if 'position' in employee.__dict__ and employee.position:
            response.position = PositionViewModel.from_model(employee.position)

        return response


class EmployeeTaskResponse(BaseModel):
    employee: EmployeeResponse | None = None
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


class ControllerTaskResponse(BaseModel):
    employee: EmployeeResponse | None = None

    @staticmethod
    def from_model(employee: Employee):
        return ControllerTaskResponse(
            employee=EmployeeResponse.from_model(employee)
        )


class TaskViewModel(BaseModel):
    title: str
    description: str | None
    priority: TaskPriorityEnum | None
    deadline: datetime | None
    deadline_end: datetime | None = None

    department_id: int | None
    controller_ids: List[int] | None = None
    executors_ids: List[int] | None = None


class TaskExecutorViewModel(BaseModel):
    employee_id: int


class TaskCommentViewModel(BaseModel):
    text: str


class TaskStatusViewModel(BaseModel):
    status: TaskStatusEnum


class TaskCommentResponse(BaseModel):
    id: int
    task_id: int
    employee_id: int | None = None
    text: str
    created_at: datetime | None = None
    updated_at: datetime | None = None

    employee: EmployeeResponse | None = None

    @staticmethod
    def from_model(task_comment: TaskComment):
        response = TaskCommentResponse(
            id=task_comment.id,
            employee_id=task_comment.employee_id,
            task_id=task_comment.task_id,
            text=task_comment.text,
            created_at=task_comment.created_at,
            updated_at=task_comment.updated_at,
        )
        if 'employee' in task_comment.__dict__ and task_comment.employee:
            response.employee = EmployeeResponse.from_model(task_comment.employee)
        return response


class TaskResponse(BaseModel):
    id: int
    created_by_id: int
    status: TaskStatusEnum
    title: str
    description: str | None
    priority: TaskPriorityEnum | None
    deadline: datetime | None
    deadline_end: datetime | None

    department_id: int | None

    department: DepartmentResponse | None = None
    executors: List[EmployeeTaskResponse] | None = None
    created_by: EmployeeResponse | None = None
    controllers: List[ControllerTaskResponse] | None = None
    comments: List[TaskCommentResponse] | None = None

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
            deadline_end=task.deadline_end,
            department_id=task.department_id,
            status=task.status,
            created_by_id=task.created_by_id,
            created_at=task.created_at,
            updated_at=task.updated_at
        )
        if 'department' in task.__dict__ and task.department:
            response.department = DepartmentResponse.from_model(task.department)

        if 'executors' in task.__dict__ and task.executors:
            response.executors = list(map(lambda e: EmployeeTaskResponse.from_model(e), task.executors))

        if 'created_by' in task.__dict__ and task.created_by:
            response.created_by = EmployeeResponse.from_model(task.created_by)

        if 'controllers' in task.__dict__ and task.controllers:
            response.controllers = list(map(lambda e: ControllerTaskResponse.from_model(e), task.controllers))

        if 'comments' in task.__dict__:
            response.comments = list(map(lambda tc: TaskCommentResponse.from_model(tc), task.comments))

        return response
