from datetime import date
from typing import Annotated

from sqlalchemy import or_
from sqlalchemy.orm import sessionmaker, joinedload
from fastapi import Depends

from app.core.models.organization import Employee
from app.dal import get_session
from app.core.models.tasks import Task


class GetTasksUseCase:
    def __init__(self,
                 session: Annotated[sessionmaker, Depends(get_session)],
                 ):
        self.session = session

    def execute(self,
                department_id: int | None,
                executor_id: int | None,
                status: str | None,
                priority: str | None,
                deadline: date | None,
                search: str | None
                ):
        with self.session() as session:
            query = session.query(Task).options(
                joinedload(Task.department),
                joinedload(Task.executor).joinedload(Employee.user),
                joinedload(Task.created_by).joinedload(Employee.user)
            )
            if department_id:
                query = query.filter(Task.department_id == department_id)
            if executor_id:
                query = query.filter(Task.executor_id == executor_id)
            if status:
                query = query.filter(Task.status == status)
            if priority:
                query = query.filter(Task.priority == priority)
            if deadline:
                query = query.filter(Task.deadline == date)
            if search:
                query = query.filter(
                    or_(Task.title.ilike(f'%{search}%'), Task.description.ilike(f'%{search}%'))
                )
            return query.all()
