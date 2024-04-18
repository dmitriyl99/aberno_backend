from typing import Annotated, List
from datetime import date

from fastapi import APIRouter, Depends, status

from .view_models import RollCallViewModel, RollCallResponse, RollCallSickLeaveResponse

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
        get_roll_call_history_use_case: Annotated[GetRollCallHistoryUseCase, Depends(GetRollCallHistoryUseCase)],
        date_from: date | None = None,
        date_to: date | None = None
):
    user = Auth.get_current_user()
    roll_call_history = get_roll_call_history_use_case.execute(user, date_from, date_to)

    return list(map(lambda roll_call: RollCallResponse(
        id=roll_call.id,
        status=roll_call.status,
        note=roll_call.note,
        created_at=roll_call.created_at,
        updated_at=roll_call.updated_at,
        sick_leave=RollCallSickLeaveResponse(
            id=roll_call.sick_leave.id,
            date_from=roll_call.sick_leave.date_from,
            date_to=roll_call.sick_leave.date_to,
            note=roll_call.sick_leave.note
        ) if roll_call.sick_leave else None
    ), roll_call_history))
