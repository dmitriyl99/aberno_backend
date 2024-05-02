from typing import Annotated, Type

from sqlalchemy.orm import sessionmaker
from fastapi import Depends

from app.core.facades.auth import Auth
from app.dal import get_session
from app.core.models.organization import Department, Employee
from app.routers.admin.view_models import CreateDepartmentViewModel


class CreateDepartmentUseCase:
    def __init__(self,
                 session: Annotated[sessionmaker, Depends(get_session)],
                 ):
        self.session = session

    def execute(self, department_view_model: CreateDepartmentViewModel) -> Department:
        current_user = Auth.get_current_user()
        department = Department(
            name=department_view_model.name,
            organization_id=department_view_model.organization_id
        )

        with self.session() as session:
            if not current_user.is_super_admin:
                current_employee: Type[Employee] = session.query(Employee).filter(
                    Employee.user_id == current_user.id
                ).first()
                department.organization_id = current_employee.organization_id
            session.add(department)
            session.commit()
            session.refresh(department)
        return department
