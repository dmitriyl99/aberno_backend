from typing import Annotated

from fastapi import APIRouter, HTTPException, status
from fastapi import Depends

from .view_models import Token, LoginForm, CurrentUserViewModel, RoleViewModel, PermissionViewModel

from app.use_cases.auth.create_token_use_case import CreateTokenUseCase
from app.dependencies import get_current_user
from app.dal.models.auth.user import User


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


@router.get("/me/")
async def get_me(
        current_user: Annotated[User, Depends(get_current_user)]
):
    await current_user.fetch_related('roles', 'permissions', 'employee')
    return CurrentUserViewModel(
        id=current_user.id,
        name=current_user.name,
        phone=current_user.phone,
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
