from app.core.models.auth.user import User
from app.core.services.auth import JWTAuthService
from passlib.context import CryptContext


class CreateTokenUseCase:
    pwd_context: CryptContext

    def __init__(self):
        self.pwd_context = CryptContext(schemes=['bcrypt'], deprecated="auto")

    async def execute(self, phone: str, password: str) -> dict | None:
        user = await User.filter(phone=phone).first()
        if user is None:
            return None
        password_verified = self.pwd_context.verify(password, user.password)
        if not password_verified:
            return None
        access_token = JWTAuthService.generate_token(subject={"sub": str(user.id)})

        return {
            'access_token': access_token,
            'type': 'bearer'
        }

