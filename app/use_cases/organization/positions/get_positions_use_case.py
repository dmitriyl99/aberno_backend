from typing import Annotated, List, Type

from fastapi import Depends
from sqlalchemy.orm import sessionmaker

from app.core.facades.auth import Auth
from app.core.models.organization.position import Position
from app.dal import get_session
from app.tasks.organization.get_current_employee_task import GetCurrentEmployeeTask


class GetPositionsUseCase:
    def __init__(
            self,
            session: Annotated[sessionmaker, Depends(get_session)],
            get_current_employee_task: Annotated[GetCurrentEmployeeTask, Depends(GetCurrentEmployeeTask)]
    ):
        self.session = session
        self.get_current_employee_task = get_current_employee_task

    def execute(self, organization_id: int | None, department_id: int | None) -> List[Position] | List[Type[Position]]:
        current_user = Auth.get_current_user()
        current_employee = self.get_current_employee_task.run(current_user)
        if (organization_id and not current_user.is_super_admin) or (not organization_id):
            organization_id = current_employee.organization_id
        with self.session() as session:
            query = session.query(Position)
            if organization_id:
                query = query.filter(Position.organization_id == organization_id)
            if department_id:
                query = query.filter(Position.department_id == department_id)
            return query.all()