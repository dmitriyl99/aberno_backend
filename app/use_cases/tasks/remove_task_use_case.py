from typing import Annotated

from sqlalchemy.orm import sessionmaker, joinedload
from fastapi import Depends, HTTPException
from starlette import status

from app.dal import get_session
from app.core.models.tasks import Task
from app.core.facades.auth import Auth
from app.tasks.organization.get_current_employee_task import GetCurrentEmployeeTask


class RemoveTaskUseCase:
    def __init__(self,
                 session: Annotated[sessionmaker, Depends(get_session)],
                 get_current_employee_task: Annotated[GetCurrentEmployeeTask, Depends(GetCurrentEmployeeTask)]
                 ):
        self.session = session
        self.get_current_employee_task = get_current_employee_task

    def execute(self,
                task_id: int
                ):
        current_user = Auth.get_current_user()
        current_employee = self.get_current_employee_task.run(current_user)
        with self.session() as session:
            task: Task = session.query(Task).options(
                joinedload(Task.comments),
                joinedload(Task.executors),
                joinedload(Task.controllers)
            ).get(task_id)
            if not task:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Task not found"
                )
            if not current_user.is_admin and not current_user.is_super_admin and (
                    not current_employee.id == task.created_by_id):
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail='You do not have permission to perform this action'
                )
            task.comments.clear()
            task.executors.clear()
            task.controllers.clear()
            session.delete(task)
            session.commit()
