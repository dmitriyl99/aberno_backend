from typing import Annotated, Type

from fastapi import Depends
from sqlalchemy.orm import sessionmaker

from app.core.models.auth.user import User
from app.dal import get_session


class GetUserByUsernameTask:
    def __init__(self, session: Annotated[sessionmaker, Depends(get_session)]):
        self.session = session

    def run(self, username: str) -> Type[User]:
        with self.session() as session:
            user = session.query(User).filter(User.username == username).first()
        return user
