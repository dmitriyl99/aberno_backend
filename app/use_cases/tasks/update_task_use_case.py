from typing import Annotated
from sqlalchemy.orm import sessionmaker
from fastapi import Depends, HTTPException
from starlette import status

from app.core.models.organization import Employee
from app.dal import get_session
from app.core.models.tasks import Task, TaskStatusEnum
from app.routers.tasks.view_models import TaskViewModel
from app.core.facades.auth import Auth
from app.tasks.organization.get_current_employee_task import GetCurrentEmployeeTask
from app.tasks.send_notification_task import SendNotificationTask


class UpdateTaskUseCase:
    def __init__(self,
                 session: Annotated[sessionmaker, Depends(get_session)],
                 get_current_employee_task: Annotated[GetCurrentEmployeeTask, Depends(GetCurrentEmployeeTask)],
                 send_notification_task: Annotated[SendNotificationTask, Depends(SendNotificationTask)]
                 ):
        self.session = session
        self.get_current_employee_task = get_current_employee_task
        self.send_notification_task = send_notification_task

    def execute(self, task_id: int, dto: TaskViewModel):
        current_user = Auth.get_current_user()
        current_employee = self.get_current_employee_task.run(current_user)
        with self.session() as session:
            task: Task = session.query(Task).get(task_id)
            if not current_user.is_super_admin or not current_user.is_admin:
                if current_employee.id != task.created_by_id:
                    raise HTTPException(
                        status_code=status.HTTP_403_FORBIDDEN,
                        detail='You do not have permission to update this task'
                    )
            task.title = dto.title
            task.description = dto.description
            task.priority = dto.priority.value
            task.deadline = dto.deadline
            task.deadline_end = dto.deadline_end
            task.department_id = dto.department_id
            if dto.controller_ids is not None:
                task.controllers.clear()
                for controller_id in dto.controller_ids:
                    employee = session.query(Employee).filter(Employee.id == controller_id).first()
                    if employee:
                        task.controllers.append(employee)
            # task.controller_employee_id = dto.controller_id
            session.commit()
            session.refresh(task)
            session.refresh(task.department)
            session.refresh(task.executors)
            session.refresh(task.controllers)
            session.refresh(task.created_by)

            return task
