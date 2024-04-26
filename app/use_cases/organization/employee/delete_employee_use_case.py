from typing import Annotated

from sqlalchemy.orm import sessionmaker
from fastapi import Depends, HTTPException, status

from app.core.models.auth import User
from app.dal import get_session
from app.core.models.organization import Employee
from app.tasks.organization.get_current_employee_task import GetCurrentEmployeeTask


class DeleteEmployeeUseCase:
    def __init__(self,
                 session: Annotated[sessionmaker, Depends(get_session)],
                 get_current_employee_task: Annotated[GetCurrentEmployeeTask, Depends(GetCurrentEmployeeTask)],
                 ):
        self.session = session
        self.get_current_employee_task = get_current_employee_task

    def execute(self, user: User, employee_id: int) -> bool:
        current_employee = self.get_current_employee_task.run(user)
        with self.session() as session:
            employee: Employee = session.query(Employee).get(employee_id)
            if not employee:
                return False
            if employee.organization_id != current_employee.organization_id:
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail="You do not have permission to delete employees not from your organization"
                )
            session.delete(employee)
            session.commit()
        return True
