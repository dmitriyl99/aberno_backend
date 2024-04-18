from typing import Annotated, List, Type

from fastapi import Depends
from sqlalchemy.orm import sessionmaker

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

    def execute(self, user: User) -> List[Type[RollCall]]:
        employee = self.get_current_employee_task.run(user)

        with self.session() as session:
            return session.query(RollCall).filter(RollCall.employee_id == employee.id).all()
