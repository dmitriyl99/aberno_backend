from typing import Annotated
from fastapi import Depends
from app.core.models.auth.user import User
from sqlalchemy.orm import sessionmaker, joinedload
from app.dal import get_session


class GetUserByIdTask:
    def __init__(self, session: Annotated[sessionmaker, Depends(get_session)]):
        self.session = session

    def run(self, id: int) -> User | None:
        with self.session() as session:
            user = session.query(User).options(
                joinedload(User.roles), joinedload(User.permissions)
            ).filter(User.id == id).first()
        return user
