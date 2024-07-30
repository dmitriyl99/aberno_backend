from typing import Annotated, List, Type, Tuple

from fastapi import Depends
from sqlalchemy.orm import sessionmaker

from app.core.facades.auth import Auth
from app.core.models.organization.position import Position
from app.dal import get_session
from app.tasks.organization.get_current_employee_task import GetCurrentEmployeeTask


class GetPositionByIdUseCase:
    def __init__(
            self,
            session: Annotated[sessionmaker, Depends(get_session)],
            get_current_employee_task: Annotated[GetCurrentEmployeeTask, Depends(GetCurrentEmployeeTask)]
    ):
        self.session = session
        self.get_current_employee_task = get_current_employee_task

    def execute(self, position_id: int) -> Position | Type[Position] | None:
        current_user = Auth.get_current_user()
        current_employee = self.get_current_employee_task.run(current_user)
        organization_id = current_employee.organization_id
        with self.session() as session:
            query = session.query(Position).filter(
                Position.organization_id == organization_id
            ).filter(Position.id == position_id)
            return query.first()
