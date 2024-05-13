from typing import Annotated
from sqlalchemy.orm import sessionmaker
from fastapi import Depends

from app.dal import get_session
from app.core.models.tasks import Task, TaskStatusEnum
from app.routers.tasks.view_models import TaskViewModel
from app.core.facades.auth import Auth
from app.tasks.organization.get_current_employee_task import GetCurrentEmployeeTask
from app.tasks.send_notification_task import SendNotificationTask


class CreateTaskUseCase:
    def __init__(self,
                 session: Annotated[sessionmaker, Depends(get_session)],
                 get_current_employee_task: Annotated[GetCurrentEmployeeTask, Depends(GetCurrentEmployeeTask)],
                 send_notification_task: Annotated[SendNotificationTask, Depends(SendNotificationTask)]
                 ):
        self.session = session
        self.get_current_employee_task = get_current_employee_task
        self.send_notification_task = send_notification_task

    def execute(self, dto: TaskViewModel):
        current_user = Auth.get_current_user()
        current_employee = self.get_current_employee_task.run(current_user)
        with self.session() as session:
            task = Task(
                title=dto.title,
                description=dto.description,
                status=TaskStatusEnum.PENDING.value,
                priority=dto.priority.value,
                deadline=dto.deadline,
                organization_id=current_employee.organization_id,
                department_id=dto.department_id,
                executor_id=dto.executor_id,
                created_by_id=current_employee.id
            )
            session.add(task)
            session.commit()
            session.refresh(task)
            session.refresh(task.department)
            session.refresh(task.executor)
            session.refresh(task.created_by)

            if task.executor:
                self.send_notification_task.run(
                    f"Вам назначена задача {task.title}",
                    "Нажмите, чтобы посмотреть",
                    task.executor.user_id
                )

            return task
