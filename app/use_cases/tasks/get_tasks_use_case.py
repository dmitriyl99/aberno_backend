from datetime import date
from typing import Annotated

from sqlalchemy import or_
from sqlalchemy.orm import sessionmaker, joinedload
from fastapi import Depends

from app.core.models.auth import User
from app.core.models.organization import Employee
from app.core.models.tasks.task import EmployeesTasks
from app.dal import get_session
from app.core.models.tasks import Task
from app.core.facades.auth import Auth
from app.tasks.organization.get_current_employee_task import GetCurrentEmployeeTask


class GetTasksUseCase:
    def __init__(self,
                 session: Annotated[sessionmaker, Depends(get_session)],
                 get_current_employee_task: Annotated[GetCurrentEmployeeTask, Depends(GetCurrentEmployeeTask)]
                 ):
        self.session = session
        self.get_current_employee_task = get_current_employee_task

    def execute(self,
                department_id: int | None,
                executor_id: int | None,
                controller_id: int | None,
                status: str | None,
                priority: str | None,
                deadline: date | None,
                search: str | None,
                created_by_id: int | None,
                page: int = 1,
                per_page: int = 10
                ):
        current_user = Auth.get_current_user()
        current_employee = self.get_current_employee_task.run(current_user)
        with self.session() as session:
            query = session.query(Task).options(
                joinedload(Task.department),
                joinedload(Task.executors).joinedload(EmployeesTasks.employee).joinedload(Employee.user),
                joinedload(Task.created_by).joinedload(Employee.user),
                joinedload(Task.controllers).joinedload(Employee.user)
            ).filter(Task.organization_id == current_employee.organization_id)
            if department_id and department_id != 0:
                query = query.filter(Task.department_id == department_id)
            if executor_id and executor_id != 0:
                query = query.filter(Task.executors.any(EmployeesTasks.employee_id == executor_id))
            if controller_id and controller_id != 0:
                query = query.filter(Task.controllers.any(Employee.id == executor_id))
            if status:
                statuses = status.split(',')
                query = query.filter(Task.status.in_(statuses))
            if priority:
                query = query.filter(Task.priority == priority)
            if deadline and deadline != 0:
                query = query.filter(Task.deadline == deadline)
            if created_by_id:
                query = query.filter(Task.created_by_id == created_by_id)
            if search:
                query = query.filter(
                    or_(Task.title.ilike(f'%{search}%'), Task.description.ilike(f'%{search}%'),
                        Task.created_by.has(Employee.user.has(User.name.ilike(f'f%{search}%'))),
                        Task.executors.has(
                            EmployeesTasks.employee.has(Employee.user.has(User.name.ilike(f'%{search}%'))))
                        )
                )
            query = query.order_by(Task.created_at.desc())
            count = query.count()
            query = query.limit(per_page).offset((page - 1) * per_page)
            return query.all(), count
