from typing import Annotated

from sqlalchemy import and_
from sqlalchemy.orm import sessionmaker
from fastapi import Depends, HTTPException, status
from passlib.context import CryptContext

from app.core.models.auth import User, Role
from app.dal import get_session
from app.core.models.organization import Employee
from app.routers.admin.view_models import CreateEmployeeViewModel
from app.tasks.organization.get_current_employee_task import GetCurrentEmployeeTask
from .change_employee_role_use_case import ChangeEmployeeRoleUseCase


class UpdateEmployeeUseCase:
    def __init__(self,
                 session: Annotated[sessionmaker, Depends(get_session)],
                 get_current_employee_task: Annotated[GetCurrentEmployeeTask, Depends(GetCurrentEmployeeTask)],
                 change_employee_role_use_case: Annotated[ChangeEmployeeRoleUseCase, Depends(ChangeEmployeeRoleUseCase)]
                 ):
        self.session = session
        self.get_current_employee_task = get_current_employee_task
        self.change_employee_role_use_case = change_employee_role_use_case
        self.pwd_context = CryptContext(schemes=['bcrypt'], deprecated="auto")

    def execute(self, current_user: User, employee_id: int,
                data: CreateEmployeeViewModel) -> Employee | None:
        current_employee = self.get_current_employee_task.run(current_user)
        error = HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail='You do not have permission to perform this action'
        )
        with self.session() as session:
            employee = session.query(Employee).filter(
                and_(Employee.organization_id == current_employee.organization_id, Employee.id == employee_id)
            ).first()
            if employee is None:
                return None
            # count_users_with_username = session.query(User).filter(and_(
            #     User.username == data.username,
            #     User.id != employee.user_id
            # )).count()
            # if count_users_with_username > 0:
            #     raise HTTPException(
            #         status_code=status.HTTP_400_BAD_REQUEST,
            #         detail='Username is already taken'
            #     )
            user: User = session.query(User).get(employee.user_id)
            if user is None:
                return None
            employee.department_id = data.department_id
            employee.position_id = data.position_id
            phone = data.phone
            if phone.startswith('+'):
                phone = phone[1:]
            employee.phone = phone
            user.name = data.name
            user.last_name = data.last_name
            if data.password:
                if data.password != data.password_confirmation:
                    raise HTTPException(status_code=400, detail="Incorrect password confirmation")
                user.password = self.pwd_context.hash(data.password)
            if data.role_id:
                role: Role = session.query(Role).get(data.role_id)
                if role.name in ['Super Admin', 'Admin'] and not current_user.is_super_admin:
                    raise error
                if current_employee.organization_id != employee.organization_id and not current_user.is_super_admin:
                    raise error
                if not current_user.is_admin and not current_user.is_super_admin:
                    raise error
                user.roles.clear()
                user.roles.append(role)
            session.commit()
            session.refresh(employee)
            session.refresh(employee.user)
            session.refresh(employee.department)
            session.refresh(employee.position)
        return employee
