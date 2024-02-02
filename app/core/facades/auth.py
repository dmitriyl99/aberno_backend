from fastapi import HTTPException, status
from jose import JWTError

from ..services.auth import JWTAuthService
from app.dal.models.auth.user import User
from app.tasks.auth.get_user_by_id_task import GetUserByIdTask


class Auth:
    __current_user: User | None

    @staticmethod
    async def authorize_user(
            token: str, token_type: str, get_user_by_id_task: GetUserByIdTask
    ):
        credentials_exception = HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
        if token_type == 'jwt':
            service = JWTAuthService()
            user_id: str = service.authorize_token(token)
            if user_id is None:
                raise credentials_exception
            user = await get_user_by_id_task.run(int(user_id))
            if user is None:
                raise credentials_exception
            Auth.__current_user = user
        else:
            raise Exception("Invalid token type")

    @staticmethod
    def get_current_user() -> User | None:
        return Auth.__current_user
