from typing import Annotated

from sqlalchemy.orm import sessionmaker
from fastapi import Depends

from app.dal import get_session
from app.core.models.organization import Organization
from app.routers.superadmin.view_mdoels import CreateOrganizationViewModel


class UpdateOrganizationUseCase:
    def __init__(self,
                 session: Annotated[sessionmaker, Depends(get_session)],
                 ):
        self.session = session

    def execute(self, organization_id: int,
                organization_view_model: CreateOrganizationViewModel) -> Organization | None:
        with self.session() as session:
            organization: Organization = session.query(Organization).get(organization_id)
            if organization is None:
                return None
            organization.name = organization_view_model.name
            organization.legal_name = organization_view_model.legal_name
            organization.legal_name_prefix = organization_view_model.legal_name_prefix
            organization.location_lat = organization_view_model.location_lat
            organization.location_lng = organization_view_model.location_lng
            session.commit()
            session.refresh(organization)
        return organization
