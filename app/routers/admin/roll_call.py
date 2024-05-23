from datetime import datetime
from typing import Annotated, List

from fastapi import APIRouter, Depends, status, HTTPException

from app.routers.roll_call.view_models import RollCallViewModel, RollCallResponse
from app.use_cases.roll_call import UpdateRollCallUseCase, DeleteRollCallUseCase, GetAllRollCallsUseCase

router = APIRouter(prefix='/roll-call', tags=['admin-roll-call'])


@router.put('/{roll_call_id}', response_model=RollCallResponse)
async def update_roll_call(
        roll_call_id: int,
        dto: RollCallViewModel,
        update_roll_call_use_case: Annotated[UpdateRollCallUseCase, Depends(UpdateRollCallUseCase)]
):
    roll_call = update_roll_call_use_case.execute(roll_call_id, dto)
    return RollCallResponse.from_model(roll_call)


@router.get('/', response_model=List[RollCallResponse])
async def get_roll_calls(
        get_roll_call_use_case: Annotated[GetAllRollCallsUseCase, Depends(GetAllRollCallsUseCase)],
        organization_id: int | None,
        department_id: int | None,
        filter_date: datetime | None = None,
        position_id: int | None = None,
        page: int | None = None,
        page_size: int = 10,
):
    count, roll_calls = get_roll_call_use_case.execute(
        organization_id,
        department_id,
        filter_date,
        position_id,
        page,
        page_size
    )

    return {
        'count': count,
        'data': list(
            map(
                lambda rc: RollCallResponse.from_model(rc), roll_calls
            )
        )
    }


@router.delete('/{roll_call_id}', status_code=status.HTTP_204_NO_CONTENT)
async def delete_roll_call(
        roll_call_id: int,
        delete_roll_call_use_case: Annotated[DeleteRollCallUseCase, Depends(DeleteRollCallUseCase)]
):
    delete_roll_call_use_case.execute(roll_call_id)
