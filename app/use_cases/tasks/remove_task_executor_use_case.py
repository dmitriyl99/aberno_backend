from typing import Annotated

from sqlalchemy.orm import sessionmaker, joinedload
from fastapi import Depends, HTTPException, status

from app.core.models.organization import Employee
from app.core.models.tasks.task import EmployeesTasks
from app.dal import get_session
from app.core.facades.auth import Auth
from app.core.models.tasks import TaskStatusEnum, Task
from app.tasks.organization.get_current_employee_task import GetCurrentEmployeeTask
from app.tasks.send_notification_task import SendNotificationTask
from app.use_cases.organization.employee import GetEmployeeByIdUseCase


class RemoveTaskExecutorUseCase:
    def __init__(
            self,
            session: Annotated[sessionmaker, Depends(get_session)],
            send_notification_task: Annotated[SendNotificationTask, Depends(SendNotificationTask)],
            get_current_employee_task: Annotated[GetCurrentEmployeeTask, Depends(GetCurrentEmployeeTask)],
            get_employee_by_id_use_case: Annotated[GetEmployeeByIdUseCase, Depends(GetEmployeeByIdUseCase)]
    ):
        self.session = session
        self.send_notification_task = send_notification_task
        self.get_current_employee_task = get_current_employee_task
        self.get_employee_by_id_use_case = get_employee_by_id_use_case

    def execute(self, task_id: int, employee_id: int) -> Task:
        current_user = Auth.get_current_user()
        current_employee = self.get_current_employee_task.run(current_user)
        with self.session() as session:
            task: Task = session.query(Task).options(
                joinedload(Task.created_by),
                joinedload(Task.executors).options(joinedload(Employee.user), joinedload(Employee.department))
            ).get(task_id)
            employee = self.get_employee_by_id_use_case.execute(current_user, employee_id)
            if employee is None:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail=f"Employee with id {employee_id} not found"
                )
            if not current_user.is_super_admin or not current_user.is_admin:
                if current_employee.id != task.created_by_id:
                    raise HTTPException(
                        status_code=status.HTTP_403_FORBIDDEN,
                        detail='You do not have permission to update this task'
                    )
            executors_with_id = list(filter(lambda e: e.id == employee_id, task.executors))
            executor_exists = len(executors_with_id) > 0
            if not executor_exists:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail='This executor already not involved in this task'
                )
            executor = executors_with_id[0]
            session.delete(executor)
            session.commit()
            session.refresh(task)
            session.refresh(task.executors)

            return task
