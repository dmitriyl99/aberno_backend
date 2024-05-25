from typing import Annotated

from sqlalchemy import and_
from sqlalchemy.orm import sessionmaker
from fastapi import Depends, HTTPException, status
from passlib.context import CryptContext

from app.core.models.auth import User
from app.dal import get_session
from app.core.models.organization import Employee
from app.routers.admin.view_models import CreateEmployeeViewModel
from app.tasks.organization.get_current_employee_task import GetCurrentEmployeeTask


class UpdateEmployeeUseCase:
    def __init__(self,
                 session: Annotated[sessionmaker, Depends(get_session)],
                 get_current_employee_task: Annotated[GetCurrentEmployeeTask, Depends(GetCurrentEmployeeTask)],
                 ):
        self.session = session
        self.get_current_employee_task = get_current_employee_task
        self.pwd_context = CryptContext(schemes=['bcrypt'], deprecated="auto")

    def execute(self, current_user: User, employee_id: int,
                data: CreateEmployeeViewModel) -> Employee | None:
        current_employee = self.get_current_employee_task.run(current_user)
        with self.session() as session:
            employee = session.query(Employee).filter(
                and_(Employee.organization_id == current_employee.organization_id, Employee.id == employee_id)
            ).first()
            if employee is None:
                return None
            count_users_with_username = session.query(User).filter(and_(
                User.username == data.username,
                User.id != employee.user_id
            )).count()
            if count_users_with_username > 0:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail='Username is already taken'
                )
            count_employees_with_phone = session.query(Employee).filter(and_(
                Employee.phone == data.phone,
                Employee.id != employee.id
            )).count()
            if count_employees_with_phone > 0:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail='Phone number is already taken'
                )
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
            if data.password:
                if data.password != data.password_confirmation:
                    raise HTTPException(status_code=400, detail="Incorrect password confirmation")
                user.password = self.pwd_context.hash(data.password)
            session.commit()
            session.refresh(employee)
            session.refresh(employee.user)
            session.refresh(employee.department)
            session.refresh(employee.position)
        return employee
