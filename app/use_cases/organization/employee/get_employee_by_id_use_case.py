from typing import Annotated, Type

from sqlalchemy import and_
from sqlalchemy.orm import sessionmaker, joinedload
from fastapi import Depends

from app.core.models.auth import User
from app.dal import get_session
from app.core.models.organization import Employee
from app.tasks.organization.get_current_employee_task import GetCurrentEmployeeTask


class GetEmployeeByIdUseCase:
    def __init__(self,
                 session: Annotated[sessionmaker, Depends(get_session)],
                 get_current_employee_task: Annotated[GetCurrentEmployeeTask, Depends(GetCurrentEmployeeTask)],
                 ):
        self.session = session
        self.get_current_employee_task = get_current_employee_task

    def execute(self, user: User, employee_id: int) -> Type[Employee]:
        current_employee = self.get_current_employee_task.run(user)
        with self.session() as session:
            organization = session.query(Employee).options(
                joinedload(Employee.department),
                joinedload(Employee.user).joinedload(User.roles),
                joinedload(Employee.created_by)
            ).filter(and_(
                Employee.organization_id == current_employee.organization_id,
                Employee.id == employee_id
            )).first()
        return organization
