from typing import Annotated

from sqlalchemy.orm import sessionmaker, joinedload
from fastapi import Depends

from app.core.models.organization import Employee
from app.dal import get_session
from app.core.models.tasks import Task
from app.core.facades.auth import Auth
from app.tasks.organization.get_current_employee_task import GetCurrentEmployeeTask


class GetTaskByIdUseCase:
    def __init__(self,
                 session: Annotated[sessionmaker, Depends(get_session)],
                 get_current_employee_task: Annotated[GetCurrentEmployeeTask, Depends(GetCurrentEmployeeTask)]
                 ):
        self.session = session
        self.get_current_employee_task = get_current_employee_task

    def execute(self,
                task_id: int
                ):
        current_user = Auth.get_current_user()
        current_employee = self.get_current_employee_task.run(current_user)
        with self.session() as session:
            task: Task = session.query(Task).options(
                joinedload(Task.department),
                joinedload(Task.executor).joinedload(Employee.user),
                joinedload(Task.created_by).joinedload(Employee.user)
            ).get(task_id)

            if task.executor_id == current_employee.id and not task.viewed:
                task.viewed = True
                session.commit()
                session.refresh(task)
            return task
