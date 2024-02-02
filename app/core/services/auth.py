from app.settings import settings
from jose import jwt, JWTError


class JWTAuthService:
    @staticmethod
    def authorize_token(token: str) -> str | None:
        payload = jwt.decode(token, settings.secret_key, algorithms=[settings.jwt_algorithm])
        sub_data: str = payload.get('sub')

        return sub_data
