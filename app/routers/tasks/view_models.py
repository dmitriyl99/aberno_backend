from datetime import date, datetime

from pydantic import BaseModel

from app.core.models.organization import Employee, Department
from app.core.models.tasks import Task, TaskStatusEnum, TaskPriorityEnum
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
    position: str | None = None

    @staticmethod
    def from_model(employee: Employee):
        response = EmployeeResponse(
            id=employee.id,
            position=employee.position
        )
        if 'user' in employee.__dict__:
            response.user = CurrentUserViewModel.from_model(employee.user)

        return response


class TaskViewModel(BaseModel):
    title: str
    description: str | None
    priority: TaskPriorityEnum | None
    deadline: date | None

    department_id: int | None
    executor_id: int | None


class TaskStatusViewModel(BaseModel):
    status: TaskStatusEnum


class TaskResponse(TaskViewModel):
    id: int
    created_by_id: int
    status: TaskStatusEnum

    department: DepartmentResponse | None = None
    executor: EmployeeResponse | None = None
    created_by: EmployeeResponse | None = None

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
            executor_id=task.executor_id,
            status=task.status,
            created_by_id=task.created_by_id,
            created_at=task.created_at,
            updated_at=task.updated_at
        )
        if 'department' in task.__dict__ and task.department:
            response.department = DepartmentResponse.from_model(task.department)

        if 'executor' in task.__dict__ and task.executor:
            response.executor = EmployeeResponse.from_model(task.executor)

        if 'created_by' in task.__dict__ and task.executor:
            response.created_by = EmployeeResponse.from_model(task.created_by)

        return response
