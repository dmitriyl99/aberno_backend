from typing import Annotated

from sqlalchemy.orm import sessionmaker
from fastapi import Depends

from app.dal import get_session
from app.core.models.tasks import TaskStatusEnum, Task


class ChangeTaskStatusUseCase:
    def __init__(self,
                 session: Annotated[sessionmaker, Depends(get_session)],
                 ):
        self.session = session

    def execute(self, task_id: int, status: TaskStatusEnum):
        with self.session() as session:
            task = session.query(Task).get(task_id)
            task.status = status.value
            session.commit()
            session.refresh(task)

        return task
