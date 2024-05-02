from typing import Annotated

from sqlalchemy.orm import sessionmaker, joinedload
from fastapi import Depends, HTTPException, status

from app.core.facades.auth import Auth
from app.dal import get_session
from app.core.models.auth import User, Role
from app.core.models.organization import Employee
from app.tasks.organization.get_current_employee_task import GetCurrentEmployeeTask


class ReactivateEmployeeUseCase:
    def __init__(self,
                 session: Annotated[sessionmaker, Depends(get_session)],
                 get_current_employee_task: Annotated[GetCurrentEmployeeTask, Depends(GetCurrentEmployeeTask)],
                 ):
        self.session = session
        self.get_current_employee_task = get_current_employee_task

    def execute(self, employee_id: int):
        current_user = Auth.get_current_user()
        current_employee = self.get_current_employee_task.run(current_user)

        with self.session() as session:
            employee: Employee = session.query(Employee).options(joinedload(Employee.user)).get(employee_id)
            if not employee:
                return False
            if employee.organization_id != current_employee.organization_id:
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail="You do not have permission to delete employees not from your organization"
                )
            employee.user.is_active = True
            session.commit()

        return True
