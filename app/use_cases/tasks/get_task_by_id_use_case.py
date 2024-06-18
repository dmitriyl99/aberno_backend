from datetime import datetime
from typing import Annotated

from sqlalchemy.orm import sessionmaker, joinedload
from fastapi import Depends

from app.core.models.organization import Employee
from app.core.models.tasks.task import EmployeesTasks
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
                joinedload(Task.executors).joinedload(EmployeesTasks.employee).joinedload(Employee.user),
                joinedload(Task.created_by).joinedload(Employee.user),
                joinedload(Task.controller).joinedload(Employee.user),
            ).get(task_id)

            if current_employee.id in list(map(lambda et: et.employee_id, task.executors)):
                employee_task: EmployeesTasks = list(filter(lambda et: et.employee_id == current_employee.id, task.executors))[0]
                if not employee_task.viewed:
                    employee_task.viewed = True
                    employee_task.viewed_at = datetime.now()
                    session.commit()
                    session.refresh(employee_task)
            return task
