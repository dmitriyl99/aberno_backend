from typing import Annotated, Type

from sqlalchemy.orm import sessionmaker, joinedload
from fastapi import Depends

from app.core.facades.auth import Auth
from app.dal import get_session
from app.core.models.organization import Department, Employee


class GetDepartmentByIdUseCase:
    def __init__(self,
                 session: Annotated[sessionmaker, Depends(get_session)],
                 ):
        self.session = session

    def execute(self, department_id: int) -> Department | None:
        current_user = Auth.get_current_user()
        with self.session() as session:
            department: Department = session.query(Department).options(
                joinedload(Department.organization)
            ).get(department_id)
            if not current_user.is_super_admin:
                current_employee: Type[Employee] = session.query(Employee).filter(
                    Employee.user_id == current_user.id
                ).first()
                if department.organization_id != current_employee.department_id:
                    return None
        return department
