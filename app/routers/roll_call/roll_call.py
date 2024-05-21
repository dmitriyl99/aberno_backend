from typing import Annotated, List
from collections import defaultdict
from datetime import date, timedelta
import calendar
import geopy.distance

from fastapi import APIRouter, Depends, status, HTTPException

from .view_models import RollCallViewModel, RollCallResponse, RollCallLeaveWorkResponse, RollCallStatusEnum

from app.core.facades.auth import Auth
from app.dependencies import verify_authenticated_user
from app.use_cases.roll_call.create_roll_call_use_case import CreateRollCallUseCase
from app.use_cases.roll_call.get_roll_call_history_user_case import GetRollCallHistoryUseCase
from ...core.models.roll_call.roll_call import RollCall
from ...tasks.organization.get_current_employee_task import GetCurrentEmployeeTask

router = APIRouter(prefix='/roll-call', tags=['roll-call'], dependencies=[Depends(verify_authenticated_user)])


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=RollCallResponse)
async def create_roll_call(
        roll_call: RollCallViewModel,
        create_roll_call_use_case: Annotated[CreateRollCallUseCase, Depends(CreateRollCallUseCase)]
):
    user = Auth.get_current_user()
    roll_call = create_roll_call_use_case.execute(roll_call, user)

    return RollCallResponse.from_model(roll_call)


@router.get("/history/", status_code=status.HTTP_200_OK, response_model=List[RollCallResponse])
async def get_roll_call_history(
        get_roll_call_history_use_case: Annotated[GetRollCallHistoryUseCase, Depends(GetRollCallHistoryUseCase)],
        get_current_employee_task: Annotated[GetCurrentEmployeeTask, Depends(GetCurrentEmployeeTask)],
        date_from: date | None = None,
        date_to: date | None = None
):
    user = Auth.get_current_user()
    current_employee = get_current_employee_task.run(user)
    roll_call_history = get_roll_call_history_use_case.execute(user, date_from, date_to)

    result = []

    groups = defaultdict(list)
    for roll_call_item in roll_call_history:
        groups[roll_call_item.created_at.date().strftime("%Y-%m-%d")].append(roll_call_item)
    for key in groups.keys():
        if len(groups[key]) > 1:
            try:
                on_work_roll_call = list(filter(
                    lambda rci: rci.status in [RollCallStatusEnum.ON_WORK, RollCallStatusEnum.LATE], groups[key]
                ))[0]
                response_model = RollCallResponse.from_model(on_work_roll_call)
                leave_work_roll_call_list = list(filter(
                    lambda rci: rci.status == RollCallStatusEnum.LEAVE_WORK, groups[key]
                ))
                if len(leave_work_roll_call_list) == 0:
                    result.append(response_model)
                    continue
                leave_work_roll_call: RollCall = leave_work_roll_call_list[0]
                response_model.leave_work = RollCallLeaveWorkResponse(
                    leave_time=leave_work_roll_call.created_at,
                    leave_note=leave_work_roll_call.note,
                    leave_with_location=False
                )
                if leave_work_roll_call.location and current_employee.organization.settings \
                        and current_employee.organization.settings.roll_call_distance and (
                        current_employee.organization.location_lat and current_employee.organization.location_lng):
                    distance = geopy.distance.geodesic(
                        (current_employee.organization.location_lat, current_employee.organization.location_lng),
                        (leave_work_roll_call.location.lat, leave_work_roll_call.location.lng)
                    )
                    if distance.m <= current_employee.organization.settings.roll_call_distance:
                        response_model.leave_work.leave_with_location = True
                result.append(response_model)
                continue

            except IndexError:
                for rc in groups[key]:
                    result.append(RollCallResponse.from_model(rc))
                continue
        result.append(RollCallResponse.from_model(groups[key][0]))

    return result


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
        if date_roll_call and date_roll_call.status == RollCallStatusEnum.LEAVE_WORK:
            on_work_roll_call = list(
                filter(
                    lambda r: r.created_at.date() == current_date and r.status in
                              [RollCallStatusEnum.ON_WORK, RollCallStatusEnum.LATE],
                    roll_call_history
            ))
            if len(on_work_roll_call) > 0:
                date_roll_call.status = on_work_roll_call[0].status
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
