from typing import Annotated

from fastapi import Depends
from sqlalchemy.orm import sessionmaker

from app.core.models.auth import User
from app.dal import get_session


class StoreFirebaseNotificationTokenUseCase:
    def __init__(self,
                 session: Annotated[sessionmaker, Depends(get_session)]):
        self.session = session

    def execute(self, user_id: id, token: str):
        with self.session() as session:
            user: User = session.query(User).get(user_id)
            user.firebase_notification_token = token
            session.commit()
