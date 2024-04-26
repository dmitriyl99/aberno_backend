from typing import Annotated

from sqlalchemy.orm import sessionmaker
from fastapi import Depends, HTTPException, status
from passlib.context import CryptContext

from app.dal import get_session
from app.core.models.auth import User
from app.core.models.organization import Employee
from app.routers.superadmin.view_models import CreateEmployeeViewModel
from app.tasks.organization.get_current_employee_task import GetCurrentEmployeeTask


class CreateEmployeeUseCase:
    def __init__(self,
                 session: Annotated[sessionmaker, Depends(get_session)],
                 get_current_employee_task: Annotated[GetCurrentEmployeeTask, Depends(GetCurrentEmployeeTask)]
                 ):
        self.session = session
        self.pwd_context = CryptContext(schemes=['bcrypt'], deprecated="auto")
        self.get_current_employee_task = get_current_employee_task

    def execute(self, user: User, data: CreateEmployeeViewModel) -> Employee:
        if data.password is None or data.password_confirmation is None:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Password is required")
        if data.password != data.password_confirmation:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Password does not match")
        current_employee = self.get_current_employee_task.run(user)

        user = User(
            name=data.name,
            username=data.username,
            password=self.pwd_context.hash(data.password)
        )

        with self.session() as session:
            count_users_with_username = session.query(User).filter(User.username == data.username).count()
            if count_users_with_username > 0:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail='Username is already taken'
                )
            count_employees_with_phone = session.query(Employee).filter(Employee.phone == data.phone).count()
            if count_employees_with_phone > 0:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail='Phone number is already taken'
                )

            session.add(user)
            session.commit()
            session.refresh(user)
            employee = Employee(
                birth_date=data.birth_date,
                phone=data.phone,
                user_id=user.id,
                department_id=data.department_id,
                organization_id=current_employee.organization_id,
            )
            session.add(employee)
            session.commit()
            session.refresh(employee.user)
            session.refresh(employee.department)
        return employee
