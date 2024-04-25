from typing import Annotated

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer

from jose import jwt, JWTError

from app.settings import settings
from app.core.models.auth.user import User
from app.tasks.auth.get_user_by_id_task import GetUserByIdTask
from app.core.facades.auth import Auth


async def get_current_user(
        token: Annotated[str, Depends(OAuth2PasswordBearer(tokenUrl='token'))],
        get_user_by_id_task: Annotated[GetUserByIdTask, Depends(GetUserByIdTask)]
) -> User:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, settings.secret_key, algorithms=[settings.jwt_algorithm])
        user_id: str = payload.get("sub")
        if user_id is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception

    user = get_user_by_id_task.run(int(user_id))
    if user is None:
        raise credentials_exception

    return user


async def verify_authenticated_user(
        token: Annotated[str, Depends(OAuth2PasswordBearer(tokenUrl='token'))],
        get_user_by_id_task: Annotated[GetUserByIdTask, Depends(GetUserByIdTask)]
):
    await Auth.authorize_user(token, 'jwt', get_user_by_id_task)


async def verify_admin_user(
        get_user_by_id_task: Annotated[GetUserByIdTask, Depends(GetUserByIdTask)]
):
    user = Auth.get_current_user()
    error = HTTPException(
        status_code=status.HTTP_403_FORBIDDEN, detail="Could not authorize admin user"
    )
    if not user:
        raise error
    admin_role_filter = filter(
        lambda role: role.name == 'Admin', user.roles
    )

    if len(list(admin_role_filter)) == 0:
        raise error
