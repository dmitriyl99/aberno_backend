from typing import Annotated

from sqlalchemy.orm import sessionmaker
from fastapi import Depends

from app.dal import get_session
from app.core.models.organization import Department
from app.routers.superadmin.view_models import CreateDepartmentViewModel


class UpdateDepartmentUseCase:
    def __init__(self,
                 session: Annotated[sessionmaker, Depends(get_session)],
                 ):
        self.session = session

    def execute(self, department_id: int,
                department_view_model: CreateDepartmentViewModel) -> Department | None:
        with self.session() as session:
            department: Department = session.query(Department).get(department_id)
            if department is None:
                return None
            department.name = department_view_model.name
            department.organization_id = department_view_model.organization_id
            session.commit()
            session.refresh(department)
        return department
