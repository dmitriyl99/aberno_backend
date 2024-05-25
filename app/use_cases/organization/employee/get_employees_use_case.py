from typing import Annotated, List, Type, Tuple

from sqlalchemy import or_
from sqlalchemy.orm import sessionmaker, joinedload, contains_eager
from fastapi import Depends, HTTPException
from starlette import status

from app.core.models.auth import User, Role
from app.dal import get_session
from app.core.models.organization import Employee
from app.tasks.organization.get_current_employee_task import GetCurrentEmployeeTask


class GetEmployeesUseCase:
    def __init__(self,
                 session: Annotated[sessionmaker, Depends(get_session)],
                 get_current_employee_task: Annotated[GetCurrentEmployeeTask, Depends(GetCurrentEmployeeTask)],
                 ):
        self.session = session
        self.get_current_employee_task = get_current_employee_task

    def execute(
            self,
            user: User,
            search: str | None = None,
            department_id: int | None = None,
            position_id: int | None = None,
            employee_status: str | None = None,
            page: int = 1,
            per_page: int = 10
    ) -> Tuple[List[Type[Employee]], int]:
        if page <= 0 or per_page <= 0:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail='Wrong pagination settings'
            )

        current_employee = self.get_current_employee_task.run(user)
        with self.session() as session:
            query = session.query(Employee).populate_existing().options(
                joinedload(Employee.user).joinedload(User.roles),
                joinedload(Employee.department),
                joinedload(Employee.created_by),
                joinedload(Employee.position)
            ).filter(
                Employee.organization_id == current_employee.organization_id,
                Employee.user.has(User.roles.any(Role.name.in_(['Employee'])))
            )
            if search is not None:
                query = query.filter(or_(
                    Employee.user.has(User.name.ilike(f"%{search}%")),
                    Employee.user.has(User.last_name.ilike(f"%{search}")),
                    Employee.phone.ilike(f"%{search}%"),
                ))
            if department_id is not None:
                query = query.filter(Employee.department_id == department_id)
            if position_id is not None:
                query = query.filter(Employee.position_id == position_id)
            if employee_status:
                is_active_filter = employee_status == 'true'
                print(is_active_filter)
                query = query.filter(Employee.user.has(User.is_active == is_active_filter))
            return query.order_by(Employee.created_at.desc()).limit(per_page).offset((page - 1) * per_page).all(), query.count()
