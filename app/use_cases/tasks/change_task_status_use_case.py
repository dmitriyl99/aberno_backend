from typing import Annotated

from sqlalchemy.orm import sessionmaker, joinedload
from fastapi import Depends

from app.dal import get_session
from app.core.models.tasks import TaskStatusEnum, Task
from app.tasks.send_notification_task import SendNotificationTask


class ChangeTaskStatusUseCase:
    def __init__(self,
                 session: Annotated[sessionmaker, Depends(get_session)],
                 send_notification_task: Annotated[SendNotificationTask, Depends(SendNotificationTask)]
                 ):
        self.session = session
        self.send_notification_task = send_notification_task

    def execute(self, task_id: int, status: TaskStatusEnum):
        with self.session() as session:
            task: Task = session.query(Task).options(joinedload(Task.created_by)).get(task_id)
            task.status = status.value
            session.commit()
            session.refresh(task)
            session.refresh(task.created_by)

            self.send_notification_task.run(
                f"Задача {task.title} выполнена",
                "Нажмите, чтобы посмотреть",
                task.created_by.user_id
            )

        return task
