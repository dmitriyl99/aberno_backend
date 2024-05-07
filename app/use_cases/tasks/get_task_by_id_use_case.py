from typing import Annotated

from sqlalchemy.orm import sessionmaker, joinedload
from fastapi import Depends

from app.core.models.organization import Employee
from app.dal import get_session
from app.core.models.tasks import Task


class GetTaskByIdUseCase:
    def __init__(self,
                 session: Annotated[sessionmaker, Depends(get_session)],
                 ):
        self.session = session

    def execute(self,
                task_id: int
                ):
        with self.session() as session:
            return session.query(Task).options(
                joinedload(Task.department),
                joinedload(Task.executor).joinedload(Employee.user),
                joinedload(Task.created_by).joinedload(Employee.user)
            ).get(task_id)
