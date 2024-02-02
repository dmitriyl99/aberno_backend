from typing import Annotated

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer

from jose import jwt, JWTError

from app.settings import settings
from app.dal.models.auth.user import User
from app.tasks.auth.get_user_by_phone_task import GetUserByPhoneTask


async def get_current_user(
        token: Annotated[str, Depends(OAuth2PasswordBearer(tokenUrl='token'))],
        get_user_by_phone_task: Annotated[GetUserByPhoneTask, Depends(GetUserByPhoneTask)]
) -> User:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, settings.secret_key, algorithms=[settings.jwt_algorithm])
        phone: str = payload.get("sub")
        if phone is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception

    user = await get_user_by_phone_task.run(phone)
    if user is None:
        raise credentials_exception

    return user
