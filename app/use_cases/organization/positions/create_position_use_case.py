from typing import Annotated

from fastapi import Depends, HTTPException
from sqlalchemy import and_
from sqlalchemy.orm import sessionmaker
from starlette import status

from app.core.facades.auth import Auth
from app.core.models.organization.position import Position
from app.dal import get_session
from app.tasks.organization.get_current_employee_task import GetCurrentEmployeeTask


class CreatePositionUseCase:
    def __init__(
            self,
            session: Annotated[sessionmaker, Depends(get_session)],
            get_current_employee_task: Annotated[GetCurrentEmployeeTask, Depends(GetCurrentEmployeeTask)]
    ):
        self.session = session
        self.get_current_employee_task = get_current_employee_task

    def execute(self, name: str, organization_id: int| None, department_id: int | None) -> Position:
        current_user = Auth.get_current_user()
        if not(current_user.is_super_admin or current_user.is_admin):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="You do not have permission to perform this"
            )
        current_employee = self.get_current_employee_task.run(current_user)
        if organization_id and not current_user.is_super_admin:
            organization_id = current_employee.organization_id
        if not organization_id:
            organization_id = current_employee.organization_id
        with self.session() as session:
            position_exists = session.query(Position).filter(
                and_(Position.name == name, Position.organization_id == organization_id)).first()
            if position_exists:
                raise HTTPException(status_code=status.HTTP_409_CONFLICT,
                                    detail="Position with this name already exists")
            position = Position(name=name, organization_id=organization_id, department_id=department_id)
            session.add(position)
            session.commit()
            session.refresh(position)
            return position
