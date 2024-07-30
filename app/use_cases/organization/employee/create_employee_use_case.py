import re
from typing import Annotated

from sqlalchemy.orm import sessionmaker
from fastapi import Depends, HTTPException, status
from passlib.context import CryptContext

from app.dal import get_session
from app.core.models.auth import User, Role
from app.core.models.organization import Employee, ScheduleType
from app.routers.admin.view_models import CreateEmployeeViewModel
from app.tasks.organization.get_current_employee_task import GetCurrentEmployeeTask


class CreateEmployeeUseCase:
    def __init__(self,
                 session: Annotated[sessionmaker, Depends(get_session)],
                 get_current_employee_task: Annotated[GetCurrentEmployeeTask, Depends(GetCurrentEmployeeTask)]
                 ):
        self.session = session
        self.pwd_context = CryptContext(schemes=['bcrypt'], deprecated="auto")
        self.get_current_employee_task = get_current_employee_task

    def execute(self, current_user: User, data: CreateEmployeeViewModel) -> Employee:
        def get_next_employee_number(session):
            last_user = session.query(User).order_by(User.employee_number.desc()).first()
            if last_user:
                last_number = int(last_user.employee_number)
                next_number = last_number + 1
            else:
                next_number = 1
            return f'{next_number:04}'

        if data.password is None or data.password_confirmation is None:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Password is required")
        if data.password != data.password_confirmation:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Password does not match")
        if data.role_id:
            if not current_user.is_super_admin:
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail='You do not have permission to perform this action'
                )
        current_employee = self.get_current_employee_task.run(current_user)

        with self.session() as session:
            # count_users_with_username = session.query(User).filter(User.username == data.username).count()
            # if count_users_with_username > 0:
            #     raise HTTPException(
            #         status_code=status.HTTP_400_BAD_REQUEST,
            #         detail='Username is already taken'
            #     )
            user = User(
                name=data.name,
                last_name=data.last_name,
                username=data.username,
                password=self.pwd_context.hash(data.password),
                employee_number=get_next_employee_number(session)
            )
            session.query(User).select_from()
            session.add(user)
            if data.role_id:
                role: Role = session.query(Role).get(data.role_id)
            else:
                role: Role = session.query(Role).get(0)
            user.roles.append(role)
            session.commit()
            session.refresh(user)
            organization_id = data.organization_id
            if organization_id and organization_id != current_employee.organization_id:
                if not current_user.is_super_admin:
                    organization_id = current_employee.organization_id
            if not organization_id:
                organization_id = current_employee.organization_id
            phone = data.phone
            if phone.startswith('+'):
                phone = phone[1:]
            employee = Employee(
                phone=phone,
                position_id=data.position_id,
                user_id=user.id,
                department_id=data.department_id,
                organization_id=organization_id,
                created_by_id=current_user.id,
                schedule_type=data.schedule_type.value() if data.schedule_type else ScheduleType.ORGANIZATION
            )
            session.add(employee)
            session.commit()
            session.refresh(employee.user)
            session.refresh(employee.department)
            session.refresh(employee.position)
        return employee
