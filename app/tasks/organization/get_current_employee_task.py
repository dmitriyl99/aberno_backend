from typing import Annotated, Type

from fastapi import Depends

from app.core.models.auth.user import User
from app.core.models.organization import Organization
from app.core.models.organization.employee import Employee
from app.dal import get_session

from sqlalchemy.orm import sessionmaker, joinedload


class GetCurrentEmployeeTask:
    def __init__(self, session: Annotated[sessionmaker, Depends(get_session)]):
        self.session = session

    def run(self, user: User) -> Type[Employee] | None:
        with self.session() as session:
            employee: Type[Employee] = session.query(Employee).filter(Employee.user_id == user.id).options(
                joinedload(Employee.organization).joinedload(Organization.settings),
                joinedload(Employee.department), joinedload(Employee.user)
            ).first()

        return employee
