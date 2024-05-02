from typing import Annotated, List, Type

from fastapi import Depends
from sqlalchemy.orm import sessionmaker

from app.core.models.auth import Role
from app.dal import get_session


class GetRolesUseCase:
    def __init__(self,
                 session: Annotated[sessionmaker, Depends(get_session)],
                 ):
        self.session = session

    def execute(self) -> List[Type[Role]]:
        with self.session() as session:
            return session.query(Role).all()
