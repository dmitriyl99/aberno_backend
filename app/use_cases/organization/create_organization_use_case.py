from typing import Annotated

from sqlalchemy.orm import sessionmaker
from fastapi import Depends

from app.dal import get_session
from app.core.models.organization import Organization
from app.routers.superadmin.view_models import CreateOrganizationViewModel


class CreateOrganizationUseCase:
    def __init__(self,
                 session: Annotated[sessionmaker, Depends(get_session)],
                 ):
        self.session = session

    def execute(self, organization: CreateOrganizationViewModel) -> Organization:
        organization = Organization(
            name=organization.name,
            legal_name=organization.legal_name,
            legal_name_prefix=organization.legal_name_prefix,
            location_lat=organization.location_lat,
            location_lng=organization.location_lng
        )

        with self.session() as session:
            session.add(organization)
            session.commit()
            session.refresh(organization)
        return organization
