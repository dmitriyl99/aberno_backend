from typing import Annotated, List, Type

from fastapi import APIRouter, Depends, status
from sqlalchemy import or_
from sqlalchemy.orm import sessionmaker, joinedload

from .view_models import DepartmentResponse
from ...core.facades.auth import Auth
from ...core.models.organization import Employee, Department
from ...dal import get_session
from ...dependencies import verify_authenticated_user

router = APIRouter(prefix="/departments", tags=['departments'], dependencies=[Depends(verify_authenticated_user)])


@router.get('/', status_code=status.HTTP_200_OK, response_model=List[DepartmentResponse])
async def get_departments(
        session: Annotated[sessionmaker, Depends(get_session)],
        search: str | None = None,
):
    current_user = Auth.get_current_user()
    with session() as session:
        current_employee: Type[Employee] = session.query(Employee).filter(
            Employee.user_id == current_user.id
        ).first()
        organization_id = current_employee.organization_id
        query = session.query(Department).options(
            joinedload(Department.organization)
        )
        if search is not None:
            query = query.filter(or_(
                Department.name.ilike(f"%{search}%"),
            ))
        departments = query.all()

    return list(
        map(
            lambda department: DepartmentResponse.from_model(department), departments
        )
    )