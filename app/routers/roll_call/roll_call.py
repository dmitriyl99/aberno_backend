from typing import Annotated, List
from datetime import date, timedelta
import calendar

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


@router.get("/calendar/status/", status_code=status.HTTP_200_OK)
async def get_roll_call_calendar_status(
        get_roll_call_history_use_case: Annotated[GetRollCallHistoryUseCase, Depends(GetRollCallHistoryUseCase)],
        filter_date: date | None = None
):
    if not filter_date:
        filter_date = date.today()
    start_date = filter_date.replace(day=1)
    end_date = filter_date.replace(day=calendar.monthrange(filter_date.year, filter_date.month)[1])

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
            date_roll_call = filtered_roll_calls[-1]
        result[current_date.strftime('%Y-%m-%d')] = date_roll_call.status if date_roll_call else None
        current_date += timedelta(days=1)
        print(current_date.strftime('%Y-%m-%d'))

    return result

