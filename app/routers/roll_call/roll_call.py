from typing import Annotated, List

from fastapi import APIRouter, Depends, status

from .view_models import RollCallViewModel, RollCallResponse

from app.core.facades.auth import Auth
from app.dependencies import verify_authenticated_user
from app.use_cases.roll_call.create_roll_call_use_case import CreateRollCallUseCase
from ...use_cases.roll_call.get_roll_call_history_user_case import GetRollCallHistoryUseCase

router = APIRouter(prefix='/roll-call', tags=['roll-call'], dependencies=[Depends(verify_authenticated_user)])


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=RollCallResponse)
async def create_roll_call(
        roll_call: RollCallViewModel,
        create_roll_call_use_case: Annotated[CreateRollCallUseCase, Depends(CreateRollCallUseCase)]
):
    user = Auth.get_current_user()
    roll_call = create_roll_call_use_case.execute(roll_call, user)

    return RollCallResponse(
        id=roll_call.id,
        status=roll_call.status,
        note=roll_call.note,
        created_at=roll_call.created_at,
        updated_at=roll_call.updated_at
    )


@router.get("/history/", status_code=status.HTTP_200_OK, response_model=List[RollCallResponse])
async def get_roll_call_history(
        get_roll_call_history_use_case: Annotated[GetRollCallHistoryUseCase, Depends(GetRollCallHistoryUseCase)]
):
    user = Auth.get_current_user()
    roll_call_history = get_roll_call_history_use_case.execute(user)

    return list(map(lambda roll_call: RollCallResponse(
        id=roll_call.id,
        status=roll_call.status,
        note=roll_call.note,
        created_at=roll_call.created_at,
        updated_at=roll_call.updated_at
    ), roll_call_history))
