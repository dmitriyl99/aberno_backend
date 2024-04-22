from typing import Annotated, List
from datetime import date, timedelta
import calendar

from fastapi import APIRouter, Depends, status, HTTPException

from .view_models import RollCallViewModel, RollCallResponse, RollCallSickLeaveResponse, RollCallStatusEnum

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


@router.get("/calendar/status/", status_code=status.HTTP_200_OK)
async def get_roll_call_calendar_status(
        get_roll_call_history_use_case: Annotated[GetRollCallHistoryUseCase, Depends(GetRollCallHistoryUseCase)],
        filter_date: date | None = None,
        filter_type: str = 'monthly'
):
    if not filter_date:
        filter_date = date.today()
    if filter_type not in ['monthly', 'weekly']:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail='Invalid filter type. Only "monthly" and "weekly" allowed'
        )
    start_date = filter_date.replace(day=1)
    end_date = filter_date.replace(day=calendar.monthrange(filter_date.year, filter_date.month)[1])
    if filter_type == 'weekly':
        start_date = filter_date - timedelta(days=filter_date.weekday())
        end_date = start_date + timedelta(days=6)

    roll_call_history = get_roll_call_history_use_case.execute(
        Auth.get_current_user(), start_date, end_date
    )
    result = {}
    current_date = start_date
    while current_date <= end_date:
        filtered_roll_calls = list(
            filter(
                lambda r: r.created_at.date() == current_date, roll_call_history
            ))
        date_roll_call = None
        if len(filtered_roll_calls) > 0:
            date_roll_call = filtered_roll_calls[0]
        result[current_date.strftime('%Y-%m-%d')] = date_roll_call.status if date_roll_call else None
        current_date += timedelta(days=1)

    sickness_roll_calls = filter(
        lambda r: r.status == RollCallStatusEnum.SICK, roll_call_history
    )
    for roll_call in sickness_roll_calls:
        current_date = roll_call.sick_leave.date_from
        while current_date <= roll_call.sick_leave.date_to:
            current_date_str = current_date.strftime('%Y-%m-%d')
            if current_date_str in result and not result[current_date_str]:
                result[current_date_str] = 'SICK'
            current_date += timedelta(days=1)

    return result

