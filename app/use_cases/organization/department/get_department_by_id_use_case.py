from typing import Annotated

from sqlalchemy.orm import sessionmaker, joinedload
from fastapi import Depends

from app.dal import get_session
from app.core.models.organization import Department


class GetDepartmentByIdUseCase:
    def __init__(self,
                 session: Annotated[sessionmaker, Depends(get_session)],
                 ):
        self.session = session

    def execute(self, department_id: int) -> Department:
        with self.session() as session:
            department = session.query(Department).options(
                joinedload(Department.organization)
            ).get(department_id)
        return department
