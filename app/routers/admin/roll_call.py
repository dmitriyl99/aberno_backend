from typing import Annotated

from fastapi import APIRouter, Depends, status, HTTPException

from app.routers.roll_call.view_models import RollCallViewModel, RollCallResponse
from app.use_cases.roll_call import UpdateRollCallUseCase


router = APIRouter(prefix='/roll-call', tags=['admin-roll-call'])


@router.put('/{roll_call_id}', response_model=RollCallResponse)
async def update_roll_call(
        roll_call_id: int,
        dto: RollCallViewModel,
        update_roll_call_use_case: Annotated[UpdateRollCallUseCase, Depends(UpdateRollCallUseCase)]
):
    roll_call = update_roll_call_use_case.execute(roll_call_id, dto)
    return RollCallResponse.from_model(roll_call)
