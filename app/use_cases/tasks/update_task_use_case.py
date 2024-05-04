from typing import Annotated
from sqlalchemy.orm import sessionmaker
from fastapi import Depends

from app.dal import get_session
from app.core.models.tasks import Task, TaskStatusEnum
from app.routers.tasks.view_models import TaskViewModel
from app.core.facades.auth import Auth
from app.tasks.organization.get_current_employee_task import GetCurrentEmployeeTask


class UpdateTaskUseCase:
    def __init__(self,
                 session: Annotated[sessionmaker, Depends(get_session)],
                 ):
        self.session = session

    def execute(self, task_id: int, dto: TaskViewModel):
        with self.session() as session:
            task = session.query(Task).get(task_id)
            task.title = dto.title,
            task.description = dto.description,
            task.priority = dto.priority,
            task.deadline = dto.deadline,
            task.department_id = dto.department_id,
            task.executor_id = dto.executor_id
            session.commit()
            session.refresh(task)
            session.refresh(task.department)
            session.refresh(task.executor)
            session.refresh(task.created_by)

            return task
