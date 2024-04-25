from typing import Annotated, List, Type

from sqlalchemy import or_
from sqlalchemy.orm import sessionmaker, joinedload
from fastapi import Depends

from app.dal import get_session
from app.core.models.organization import Organization


class GetOrganizationsCase:
    def __init__(self,
                 session: Annotated[sessionmaker, Depends(get_session)],
                 ):
        self.session = session

    def execute(self, search: str | None = None) -> List[Type[Organization]]:
        with self.session() as session:
            query = session.query(Organization)
            if search is not None:
                query = query.filter(or_(
                    Organization.name.ilike(f"%{search}%"),
                    Organization.legal_name.ilike(f"%{search}%"),
                ))
            return query.all()
