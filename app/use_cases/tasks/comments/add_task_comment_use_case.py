from typing import Annotated

from fastapi import Depends
from sqlalchemy.orm import sessionmaker, joinedload

from app.core.models.tasks.task import TaskComment
from app.dal import get_session
from app.core.facades.auth import Auth
from app.tasks.organization.get_current_employee_task import GetCurrentEmployeeTask


class AddTaskCommentUseCase:
    def __init__(
            self,
            session: Annotated[sessionmaker, Depends(get_session)],
            get_current_employee_task: Annotated[GetCurrentEmployeeTask, Depends(GetCurrentEmployeeTask)]
    ):
        self.session = session
        self.get_current_employee_task = get_current_employee_task

    def execute(self, task_id: int, text: str) -> TaskComment:
        current_user = Auth.get_current_user()
        current_employee = self.get_current_employee_task.run(current_user)
        task_comment = TaskComment(
            task_id=task_id,
            employee_id=current_employee.id,
            text=text
        )
        with self.session() as session:
            session.add(task_comment)
            session.commit()
            session.refresh(task_comment)
        return task_comment
