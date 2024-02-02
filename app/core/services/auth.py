from app.settings import settings
from datetime import timedelta, datetime, timezone

from jose import jwt, JWTError


class JWTAuthService:
    @staticmethod
    def authorize_token(token: str) -> str | None:
        payload = jwt.decode(token, settings.secret_key, algorithms=[settings.jwt_algorithm])
        sub_data: str = payload.get('sub')

        return sub_data

    @staticmethod
    def generate_token(subject: dict):
        to_encode = subject.copy()
        expires_delta: timedelta = timedelta(minutes=settings.access_token_expires_minutes)
        expire = datetime.now(timezone.utc) + expires_delta
        to_encode.update({"exp": expire})
        encoded_jwt = jwt.encode(to_encode, settings.secret_key, algorithm=settings.jwt_algorithm)
        return encoded_jwt
