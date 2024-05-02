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


async def _verify_user_roles(user: User, roles: list) -> bool:
    role_filter = filter(
        lambda r: r.name in roles, user.roles
    )
    return len(list(role_filter)) > 0


async def verify_admin_user():
    user = Auth.get_current_user()
    if not _verify_user_roles(user, ['Admin', 'Super Admin']):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="Could not authorize admin user"
        )


async def verify_super_admin_user():
    user = Auth.get_current_user()
    if not _verify_user_roles(user, ['Super Admin']):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="Could not authorize admin user"
        )
