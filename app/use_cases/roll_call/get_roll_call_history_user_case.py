from typing import Annotated, List, Type
from datetime import date, datetime

from fastapi import Depends
from sqlalchemy import and_
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

    def execute(self, user: User | None, date_from: date | None, date_to: date | None) -> List[Type[RollCall]]:
        employee = self.get_current_employee_task.run(user)
        with self.session() as session:
            query = session.query(RollCall).options(
                joinedload(RollCall.sick_leave),
                joinedload(RollCall.location)
            ).filter(and_(
                RollCall.organization_id == employee.organization_id,
                RollCall.employee_id == employee.id)
            ).order_by(RollCall.created_at.desc())

            if date_from:
                query = query.filter(RollCall.created_at >= date_from)
            if date_to:
                date_to = datetime(date_to.year, date_to.month, date_to.day, 23, 59, 59)
                query = query.filter(RollCall.created_at <= date_to)

            return query.all()
