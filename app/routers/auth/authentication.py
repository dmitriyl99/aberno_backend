from typing import Annotated

from fastapi import APIRouter, HTTPException, status
from fastapi import Depends

from .view_models import Token, LoginForm, CurrentUserViewModel, RoleViewModel, PermissionViewModel

from app.use_cases.auth.create_token_use_case import CreateTokenUseCase
from app.dependencies import verify_authenticated_user
from app.core.facades.auth import Auth


router = APIRouter()


@router.post("/token/")
async def create_access_token(
        form: LoginForm,
        use_case: Annotated[CreateTokenUseCase, Depends(CreateTokenUseCase)]
) -> Token:
    token_dict = use_case.execute(form.username, form.password)

    if not token_dict:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect phone or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    return Token(**token_dict)


@router.get("/me/", response_model=CurrentUserViewModel, dependencies=[Depends(verify_authenticated_user)])
async def get_me(
):
    current_user = Auth.get_current_user()
    return CurrentUserViewModel(
        id=current_user.id,
        name=current_user.name,
        username=current_user.username,
        created_at=current_user.created_at,
        updated_at=current_user.updated_at,
        roles=list(map(lambda x: RoleViewModel(
            id=x.id,
            name=x.name
        ), current_user.roles)),
        permissions=list(map(lambda x: PermissionViewModel(
            id=x.id,
            name=x.name
        ), current_user.permissions))
    )
