from typing import Annotated

from sqlalchemy.orm import sessionmaker, joinedload
from fastapi import Depends, HTTPException, status

from app.core.facades.auth import Auth
from app.dal import get_session
from app.core.models.auth import User, Role
from app.core.models.organization import Employee


class ChangeEmployeeRoleUseCase:
    def __init__(self,
                 session: Annotated[sessionmaker, Depends(get_session)],
                 ):
        self.session = session

    def execute(self, employee_id: int, role_id: int):
        current_user = Auth.get_current_user()
        with self.session() as session:
            current_user_is_super_admin = current_user.is_super_admin
            if not current_user_is_super_admin:
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail='You do not have permission to perform this action'
                )
            employee: Employee = session.query(Employee).options(joinedload(Employee.user)).get(employee_id)
            user: User = employee.user
            role = session.query(Role).get(role_id)
            user.roles.clear()
            user.roles.append(role)
            session.commit()
