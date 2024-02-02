from app.settings import settings
from datetime import timedelta, datetime, timezone

from jose import jwt


class CreateJWTTokenTask:
    expires_delta: timedelta = timedelta(minutes=settings.access_token_expires_minutes)

    def run(self, data: dict):
        to_encode = data.copy()
        expire = datetime.now(timezone.utc) + self.expires_delta
        to_encode.update({"exp": expire})
        encoded_jwt = jwt.encode(to_encode, settings.secret_key, algorithm=settings.jwt_algorithm)
        return encoded_jwt
