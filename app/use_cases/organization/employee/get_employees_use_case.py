from typing import Annotated, List, Type

from sqlalchemy import or_
from sqlalchemy.orm import sessionmaker, joinedload
from fastapi import Depends

from app.core.models.auth import User
from app.dal import get_session
from app.core.models.organization import Employee
from app.tasks.organization.get_current_employee_task import GetCurrentEmployeeTask


class GetEmployeesUseCase:
    def __init__(self,
                 session: Annotated[sessionmaker, Depends(get_session)],
                 get_current_employee_task: Annotated[GetCurrentEmployeeTask, Depends(GetCurrentEmployeeTask)],
                 ):
        self.session = session
        self.get_current_employee_task = get_current_employee_task

    def execute(self, user: User, search: str | None = None, department_id: int | None = None) -> List[Type[Employee]]:
        current_employee = self.get_current_employee_task.run(user)
        with self.session() as session:
            query = session.query(Employee).options(
                joinedload(Employee.user), joinedload(Employee.department)
            ).filter(
                Employee.organization_id == current_employee.organization_id
            )
            if search is not None:
                query = query.filter(or_(
                    User.name.ilike(f"%{search}%"),
                    Employee.phone.ilike(f"%{search}%"),
                ))
            if department_id is not None:
                query = query.filter(Employee.department_id == department_id)
            return query.all()
