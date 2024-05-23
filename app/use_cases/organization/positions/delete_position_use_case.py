from typing import Annotated

from fastapi import Depends, HTTPException
from sqlalchemy.orm import sessionmaker
from starlette import status

from app.core.facades.auth import Auth
from app.core.models.organization.position import Position
from app.dal import get_session
from app.tasks.organization.get_current_employee_task import GetCurrentEmployeeTask


class DeletePositionUseCase:
    def __init__(
            self,
            session: Annotated[sessionmaker, Depends(get_session)],
            get_current_employee_task: Annotated[GetCurrentEmployeeTask, Depends(GetCurrentEmployeeTask)]
    ):
        self.session = session
        self.get_current_employee_task = get_current_employee_task

    def execute(self, id: int):
        current_user = Auth.get_current_user()
        current_employee = self.get_current_employee_task.run(current_user)
        if not current_user.is_super_admin or not current_user.is_admin:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="You do not have permission to perform this"
            )
        with self.session() as session:
            position: Position = session.query(Position).get(id)
            if not position:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail=f"Position with id {id} does not exist"
                )
            if not current_user.is_super_admin and not position.organization_id == current_employee.organization_id:
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail="You do not have permission to perform this"
                )
            session.delete(position)
            session.commit()
