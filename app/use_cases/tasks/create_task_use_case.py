from typing import Annotated
from sqlalchemy.orm import sessionmaker
from fastapi import Depends

from app.core.models.organization import Employee
from app.core.models.tasks.task import EmployeesTasks
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
                # controller_employee_id=dto.controller_id,
                created_by_id=current_employee.id
            )
            session.add(task)
            if dto.executors_ids is not None:
                for executor_id in dto.executors_ids:
                    task.executors.append(EmployeesTasks(employee_id=executor_id, status=TaskStatusEnum.PENDING.value))
            if dto.controller_ids is not None:
                for controller_id in dto.controller_ids:
                    employee = session.query(Employee).filter(Employee.id == controller_id).first()
                    if employee:
                        task.controllers.append(employee)
            session.commit()
            session.refresh(task)
            session.refresh(task.department)
            session.refresh(task.executors)
            session.refresh(task.controllers)
            session.refresh(task.created_by)

            if task.executors:
                try:
                    for executor in task.executors:
                        self.send_notification_task.run(
                            f"Вам назначена задача {task.title}",
                            "Нажмите, чтобы посмотреть",
                            executor.employee.user_id
                        )
                except Exception:
                    pass

            return task
