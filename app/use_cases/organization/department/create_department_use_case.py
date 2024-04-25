from typing import Annotated

from sqlalchemy.orm import sessionmaker
from fastapi import Depends

from app.dal import get_session
from app.core.models.organization import Department
from app.routers.superadmin.view_models import CreateDepartmentViewModel


class CreateDepartmentUseCase:
    def __init__(self,
                 session: Annotated[sessionmaker, Depends(get_session)],
                 ):
        self.session = session

    def execute(self, department_view_model: CreateDepartmentViewModel) -> Department:
        department = Department(
            name=department_view_model.name,
            organization_id=department_view_model.organization_id
        )

        with self.session() as session:
            session.add(department)
            session.commit()
            session.refresh(department)
        return department
