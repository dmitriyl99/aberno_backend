from typing import Annotated, Tuple, List, Type

from fastapi import Depends, HTTPException, status
from sqlalchemy import or_
from sqlalchemy.orm import sessionmaker, joinedload

from app.core.models.auth import User, Role
from app.core.models.organization import Employee, Department
from app.dal import get_session
from app.tasks.organization.get_current_employee_task import GetCurrentEmployeeTask


class GetAdminsUseCase:
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
            organization_id: int | None = None,
            department_id: int | None = None,
            employee_status: str | None = None,
            role: str | None = None,
            page: int = 1,
            per_page: int = 10
    ) -> Tuple[List[Type[Employee]], int]:
        if page <= 0 or per_page <= 0:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail='Wrong pagination settings'
            )
        if not user.is_super_admin:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail='You do not have permission to perform this'
            )
        roles = ['Admin', 'Super Admin']
        if role:
            roles = [role]
        with self.session() as session:
            query = session.query(Employee).populate_existing().options(
                joinedload(Employee.user).joinedload(User.roles),
                joinedload(Employee.department).joinedload(Department.organization),
                joinedload(Employee.position),
                joinedload(Employee.created_by)
            ).filter(Employee.user.has(User.roles.any(Role.name.in_(roles))))
            if search:
                search_splitted = search.split(' ')
                if len(search_splitted) == 2:
                    query = query.filter(or_(
                        Employee.user.has(User.name.ilike(f"%{search_splitted[0]}%")),
                        Employee.user.has(User.name.ilike(f"%{search_splitted[1]}%")),
                        Employee.user.has(User.last_name.ilike(f"%{search_splitted[0]}%")),
                        Employee.user.has(User.last_name.ilike(f"%{search_splitted[1]}%")),
                        Employee.phone.ilike(f"%{search}%"),
                    ))
                else:
                    query = query.filter(or_(
                        Employee.user.has(User.name.ilike(f"%{search}%")),
                        Employee.user.has(User.last_name.ilike(f"%{search}%")),
                        Employee.phone.ilike(f"%{search}%"),
                    ))
            if organization_id:
                query = query.filter(Employee.organization_id == organization_id)
            if department_id:
                query = query.filter(Employee.department_id == department_id)
            if employee_status:
                is_active_filter = employee_status == 'true'
                print(is_active_filter)
                query = query.filter(Employee.user.has(User.is_active == is_active_filter))
            return query.order_by(Employee.created_at.desc()).limit(per_page).offset(
                (page - 1) * per_page).all(), query.count()

