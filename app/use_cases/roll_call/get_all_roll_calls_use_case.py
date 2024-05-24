from datetime import date
from typing import Annotated, List, Type, Tuple

from fastapi import Depends, HTTPException
from sqlalchemy import func
from sqlalchemy.orm import sessionmaker, joinedload
from starlette import status

from app.core.models.organization import Employee, Organization, Department
from app.core.models.roll_call.roll_call import RollCall
from app.dal import get_session
from app.core.facades.auth import Auth
from app.tasks.organization.get_current_employee_task import GetCurrentEmployeeTask


class GetAllRollCallsUseCase:
    def __init__(
            self,
            session: Annotated[sessionmaker, Depends(get_session)],
            get_current_employee_task: Annotated[GetCurrentEmployeeTask, Depends(GetCurrentEmployeeTask)]
    ):
        self.session = session
        self.get_current_employee_task = get_current_employee_task

    def execute(
            self,
            organization_id: int | None,
            department_id: int | None,
            filter_date: date | None = None,
            position_id: int | None = None
    ) -> List[RollCall] | List[Type[RollCall]]:
        current_user = Auth.get_current_user()
        current_employee = self.get_current_employee_task.run(current_user)

        if not (current_user.is_super_admin or current_user.is_admin):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="You do not have permission to perform this"
            )
        if not current_user.is_super_admin:
            organization_id = current_employee.organization_id

        with self.session() as session:
            query = session.query(RollCall).join(RollCall.employee).options(
                joinedload(RollCall.employee).options(
                    joinedload(Employee.organization).joinedload(Organization.settings),
                    joinedload(Employee.user),
                    joinedload(Employee.position), joinedload(Employee.department).joinedload(Department.organization)
                ),
                joinedload(RollCall.location)
            )
            if organization_id:
                query = query.filter(RollCall.organization_id == organization_id)
            if department_id:
                query = query.filter(RollCall.department_id == department_id)
            if position_id:
                query = query.filter(RollCall.employee.has(Employee.position_id == position_id))
            if filter_date:
                query = query.filter(func.date(RollCall.created_at) == filter_date)
            return query.order_by(RollCall.created_at.desc()).all()

