from typing import Annotated, List, Type
from datetime import date, datetime

from fastapi import Depends
from sqlalchemy.orm import sessionmaker, joinedload

from app.dal import get_session
from app.core.models.roll_call.roll_call import RollCall
from app.core.models.auth import User
from app.tasks.organization.get_current_employee_task import GetCurrentEmployeeTask


class GetRollCallHistoryUseCase:
    def __init__(self,
                 session: Annotated[sessionmaker, Depends(get_session)],
                 get_current_employee_task: Annotated[GetCurrentEmployeeTask, Depends(GetCurrentEmployeeTask)]
    ):
        self.session = session
        self.get_current_employee_task = get_current_employee_task

    def execute(self, user: User, date_from: date | None, date_to: date | None) -> List[Type[RollCall]]:
        employee = self.get_current_employee_task.run(user)

        with self.session() as session:
            query = session.query(RollCall).options(
                joinedload(RollCall.sick_leave)
            ).filter(
                RollCall.employee_id == employee.id
            ).filter(
                RollCall.organization_id == employee.organization_id
            ).filter(
                RollCall.department_id == employee.department_id
            )

            date_to = datetime(date_to.year, date_to.month, date_to.day, 23, 59, 59)

            if date_from:
                query = query.filter(RollCall.created_at >= date_from)
            if date_to:
                query = query.filter(RollCall.created_at <= date_to)

            return query.all()
