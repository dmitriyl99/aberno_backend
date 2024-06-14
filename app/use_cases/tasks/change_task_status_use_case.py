from typing import Annotated

from sqlalchemy.orm import sessionmaker, joinedload
from fastapi import Depends, HTTPException, status as fastapi_status

from app.dal import get_session
from app.core.facades.auth import Auth
from app.core.models.tasks import TaskStatusEnum, Task
from app.tasks.organization.get_current_employee_task import GetCurrentEmployeeTask
from app.tasks.send_notification_task import SendNotificationTask


class ChangeTaskStatusUseCase:
    def __init__(self,
                 session: Annotated[sessionmaker, Depends(get_session)],
                 send_notification_task: Annotated[SendNotificationTask, Depends(SendNotificationTask)],
                 get_current_employee_task: Annotated[GetCurrentEmployeeTask, Depends(GetCurrentEmployeeTask)]
                 ):
        self.session = session
        self.send_notification_task = send_notification_task
        self.get_current_employee_task = get_current_employee_task

    def execute(self, task_id: int, status: TaskStatusEnum):
        def _refresh_entity(session, task: Task):
            session.refresh(task)
            session.refresh(task.created_by)
            session.refresh(task.executors)

        def _send_notification(task: Task):
            try:
                self.send_notification_task.run(
                    f"Задача {task.title} выполнена",
                    "Нажмите, чтобы посмотреть",
                    task.created_by.user_id
                )
            except Exception:
                pass

        current_user = Auth.get_current_user()
        current_employee = self.get_current_employee_task.run(current_user)
        with self.session() as session:
            task: Task = session.query(Task).options(
                joinedload(Task.created_by),
                joinedload(Task.executors)
            ).get(task_id)
            if current_user.is_admin or current_user.is_super_admin or current_employee.id == task.created_by_id:
                task.status = status.value
                session.commit()
                _refresh_entity(session, task)
                if task.status == TaskStatusEnum.COMPLETED.value:
                    _send_notification(task)
                return task
            if current_employee.id not in list(map(lambda et: et.employee_id, task.executors)):
                raise HTTPException(
                    status_code=fastapi_status.HTTP_400_BAD_REQUEST,
                    detail='You cannot change task status'
                )
            employee_task = list(filter(lambda et: et.employee_id == current_employee.id, task.executors))[0]
            employee_task.status = status.value
            session.commit()
            _refresh_entity(session, task)

            task_completed = True
            for executor in task.executors:
                if executor.status != TaskStatusEnum.COMPLETED.value:
                    task_completed = False
            if task_completed:
                task.status = TaskStatusEnum.COMPLETED.value
                session.commit()
                _refresh_entity(session, task)
                _send_notification(task)

            if task.status == TaskStatusEnum.PENDING.value:
                task_started = False
                for executor in task.executors:
                    if executor.status == TaskStatusEnum.IN_PROGRESS.value:
                        task_started = True
                if task_started:
                    task.status = TaskStatusEnum.IN_PROGRESS.value
                    session.commit()
                    _refresh_entity(session, task)

        return task
