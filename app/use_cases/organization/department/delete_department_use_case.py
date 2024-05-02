from typing import Annotated, Type

from sqlalchemy.orm import sessionmaker
from fastapi import Depends

from app.core.facades.auth import Auth
from app.core.models.auth import User
from app.dal import get_session
from app.core.models.organization import Department, Employee


class DeleteDepartmentUseCase:
    def __init__(self,
                 session: Annotated[sessionmaker, Depends(get_session)],
                 ):
        self.session = session

    def execute(self, department_id: int) -> bool:
        current_user = Auth.get_current_user()
        with self.session() as session:
            department: Department = session.query(Department).get(department_id)
            if not current_user.is_super_admin:
                current_employee: Type[Employee] = session.query(Employee).filter(
                    Employee.user_id == current_user.id
                ).first()
                organization_id = current_employee.organization_id
                if department.organization_id != organization_id:
                    return False
            if not department:
                return False
            session.delete(department)
            session.commit()
        return True
