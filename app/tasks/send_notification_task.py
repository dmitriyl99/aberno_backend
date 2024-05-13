from typing import Annotated

from fastapi import Depends
from firebase_admin import messaging
from sqlalchemy.orm import sessionmaker

from app.core.models.auth import User
from app.dal import get_session


class SendNotificationTask:
    def __init__(self, session: Annotated[sessionmaker, Depends(get_session)]) -> None:
        self._session = session

    def run(self, title: str, body: str, user_id: int):
        with self._session() as session:
            user: User = session.query(User).get(user_id)
        if not user.firebase_notification_token:
            return
        message = messaging.Message(
            notification=messaging.Notification(
                title=title,
                body=body
            ),
            token=user.firebase_notification_token
        )
        messaging.send(message)
