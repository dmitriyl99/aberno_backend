from typing import Annotated

from sqlalchemy.orm import sessionmaker, joinedload
from fastapi import Depends

from app.dal import get_session
from app.core.models.organization import Organization


class GetOrganizationByIdUseCase:
    def __init__(self,
                 session: Annotated[sessionmaker, Depends(get_session)],
                 ):
        self.session = session

    def execute(self, organization_id: int) -> Organization:
        with self.session() as session:
            organization = session.query(Organization).options(
                joinedload(Organization.departments),
                joinedload(Organization.settings)
            ).get(organization_id)
        return organization
