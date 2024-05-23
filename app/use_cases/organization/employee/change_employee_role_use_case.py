from typing import Annotated

from sqlalchemy.orm import sessionmaker, joinedload
from fastapi import Depends, HTTPException, status

from app.core.facades.auth import Auth
from app.dal import get_session
from app.core.models.auth import User, Role
from app.core.models.organization import Employee
from app.tasks.organization.get_current_employee_task import GetCurrentEmployeeTask


class ChangeEmployeeRoleUseCase:
    def __init__(self,
                 session: Annotated[sessionmaker, Depends(get_session)],
                 get_current_employee_task: Annotated[GetCurrentEmployeeTask, Depends(GetCurrentEmployeeTask)]
                 ):
        self.session = session
        self.get_current_employee_task = get_current_employee_task

    def execute(self, employee_id: int, role_id: int):
        current_user = Auth.get_current_user()
        current_employee = self.get_current_employee_task.run(current_user)
        error = HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail='You do not have permission to perform this action'
        )

        with self.session() as session:
            employee: Employee = session.query(Employee).options(joinedload(Employee.user)).get(employee_id)
            role: Role = session.query(Role).get(role_id)
            if role.name in ['Super Admin', 'Admin'] and not current_user.is_super_admin:
                raise error
            if current_employee.organization_id != employee.organization_id and not current_user.is_super_admin:
                raise error
            if not current_user.is_admin:
                raise error
            user: User = employee.user
            user.roles.clear()
            user.roles.append(role)
            session.commit()
