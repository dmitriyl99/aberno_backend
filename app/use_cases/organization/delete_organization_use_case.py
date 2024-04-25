from typing import Annotated

from sqlalchemy.orm import sessionmaker
from fastapi import Depends

from app.dal import get_session
from app.core.models.organization import Organization


class DeleteOrganizationUseCase:
    def __init__(self,
                 session: Annotated[sessionmaker, Depends(get_session)],
                 ):
        self.session = session

    def execute(self, organization_id: int) -> bool:
        with self.session() as session:
            organization: Organization = session.query(Organization).get(organization_id)
            if not organization:
                return False
            session.delete(organization)
            session.commit()
        return True
