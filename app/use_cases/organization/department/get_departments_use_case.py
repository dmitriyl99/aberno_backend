from typing import Annotated, List, Type

from sqlalchemy import or_
from sqlalchemy.orm import sessionmaker, joinedload
from fastapi import Depends

from app.core.facades.auth import Auth
from app.dal import get_session
from app.core.models.organization import Department, Employee


class GetDepartmentsUseCase:
    def __init__(self,
                 session: Annotated[sessionmaker, Depends(get_session)],
                 ):
        self.session = session

    def execute(self, search: str | None = None,
                organization_id: int | None = None) -> List[Type[Department]]:
        current_user = Auth.get_current_user()
        with self.session() as session:
            if not current_user.is_super_admin:
                current_employee: Employee = session.query(Employee).filter(
                    Employee.user_id == current_user.id
                ).first()
                organization_id = current_employee.organization_id
            query = session.query(Department).options(
                joinedload(Department.organization)
            )
            if search is not None:
                query = query.filter(or_(
                    Department.name.ilike(f"%{search}%"),
                ))
            if organization_id is not None:
                query = query.filter(Department.organization_id == organization_id)
            return query.all()
