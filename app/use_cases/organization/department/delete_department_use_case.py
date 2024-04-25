from typing import Annotated

from sqlalchemy.orm import sessionmaker
from fastapi import Depends

from app.dal import get_session
from app.core.models.organization import Department


class DeleteDepartmentUseCase:
    def __init__(self,
                 session: Annotated[sessionmaker, Depends(get_session)],
                 ):
        self.session = session

    def execute(self, department_id: int) -> bool:
        with self.session() as session:
            department: Department = session.query(Department).get(department_id)
            if not department:
                return False
            session.delete(department)
            session.commit()
        return True
