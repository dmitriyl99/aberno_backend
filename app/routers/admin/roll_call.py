from datetime import date
from typing import Annotated
from collections import defaultdict

import geopy.distance

from fastapi import APIRouter, Depends, status

from app.core.models.roll_call.roll_call import RollCall, RollCallStatusEnum
from app.routers.roll_call.view_models import RollCallViewModel, RollCallResponse, \
    RollCallLeaveWorkResponse
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


@router.get('/')
async def get_roll_calls(
        get_roll_call_use_case: Annotated[GetAllRollCallsUseCase, Depends(GetAllRollCallsUseCase)],
        organization_id: int | None = None,
        department_id: int | None = None,
        filter_date: date | None = None,
        position_id: int | None = None,
        page: int = 1,
        per_page: int = 10,
):
    roll_calls = get_roll_call_use_case.execute(
        organization_id,
        department_id,
        filter_date,
        position_id
    )

    employee_ids = set(
        map(lambda rc: rc.employee_id, roll_calls)
    )

    result = []

    groups = defaultdict(list)
    for roll_call_item in roll_calls:
        groups[roll_call_item.created_at.date().strftime("%Y-%m-%d")].append(roll_call_item)
    for employee_id in employee_ids:
        for key in groups.keys():
            if len(groups[key]) > 1:
                try:
                    on_work_roll_call = list(filter(
                        lambda rci: rci.status in [RollCallStatusEnum.ON_WORK.value,
                                                   RollCallStatusEnum.LATE.value] and rci.employee_id == employee_id,
                        groups[key]
                    ))[0]
                    current_employee = on_work_roll_call.employee
                    response_model = RollCallResponse.from_model(on_work_roll_call)
                    leave_work_roll_call_list = list(filter(
                        lambda rci: rci.status == RollCallStatusEnum.LEAVE_WORK and rci.employee_id == employee_id,
                        groups[key]
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
                    for rc in filter(lambda rc: rc.employee_id == employee_id, groups[key]):
                        result.append(RollCallResponse.from_model(rc))
                    continue
            result.append(RollCallResponse.from_model(groups[key][0]))
    pages = [result[i:i+per_page] for i in range(0, len(result), per_page)]

    return {
        'count': len(result),
        'data': pages[page - 1] if len(pages) > 0 else []
    }


@router.delete('/{roll_call_id}', status_code=status.HTTP_204_NO_CONTENT)
async def delete_roll_call(
        roll_call_id: int,
        delete_roll_call_use_case: Annotated[DeleteRollCallUseCase, Depends(DeleteRollCallUseCase)]
):
    delete_roll_call_use_case.execute(roll_call_id)
