from typing import Annotated

from fastapi import APIRouter, HTTPException, status
from fastapi import Depends

from .view_models import Token, LoginForm, CurrentUserViewModel, FirebaseToken

from app.use_cases.auth.create_token_use_case import CreateTokenUseCase
from app.dependencies import verify_authenticated_user
from app.core.facades.auth import Auth
from ...use_cases.auth.store_firebase_notification_token_use_case import StoreFirebaseNotificationTokenUseCase

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
    return CurrentUserViewModel.from_model(current_user)


@router.post("/firebase-notification-token/", status_code=status.HTTP_204_NO_CONTENT, dependencies=[Depends(verify_authenticated_user)])
async def store_firebase_notification_token(
    store_firebase_notification_token_use_case:
    Annotated[StoreFirebaseNotificationTokenUseCase, Depends(StoreFirebaseNotificationTokenUseCase)],
        form: FirebaseToken
):
    current_user = Auth.get_current_user()
    store_firebase_notification_token_use_case.execute(current_user.id, form.token)
