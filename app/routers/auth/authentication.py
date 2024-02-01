from typing import Annotated

from fastapi import APIRouter, HTTPException, status
from fastapi import Depends, Body
from fastapi.security import OAuth2PasswordRequestForm

from .view_models import Token, LoginForm

from app.use_cases.auth.create_token_use_case import CreateTokenUseCase


router = APIRouter()


@router.post("/token/")
async def create_access_token(
        form: LoginForm,
        use_case: Annotated[CreateTokenUseCase, Depends(CreateTokenUseCase)]
) -> Token:
    token_dict = await use_case.execute(form.phone, form.password)

    if not token_dict:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect phone or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    return Token(**token_dict)
