from typing import Annotated

from fastapi import APIRouter, Depends

from .view_models import RollCallViewModel

from app.core.facades.auth import Auth
from app.dependencies import verify_authenticated_user
from app.use_cases.roll_call.create_roll_call_use_case import CreateRollCallUseCase


router = APIRouter(prefix='/roll-call', tags=['roll-call'], dependencies=[Depends(verify_authenticated_user)])


@router.post("/")
async def create_roll_call(
        roll_call: RollCallViewModel,
        create_roll_call_use_case: Annotated[CreateRollCallUseCase, Depends(CreateRollCallUseCase)]
):
    user = Auth.get_current_user()
    roll_call = create_roll_call_use_case.execute(roll_call, user)

    return roll_call
