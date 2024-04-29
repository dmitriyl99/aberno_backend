from typing import Annotated

from fastapi import Depends, HTTPException
from sqlalchemy.orm import sessionmaker
import geopy.distance
from starlette import status

from datetime import date, datetime

from app.core.models.roll_call.sick_leave import SickLeave
from app.dal import get_session
from app.routers.roll_call.view_models import RollCallViewModel, RollCallStatusEnum
from app.core.models.roll_call.roll_call import RollCall, Location
from app.core.models.auth import User
from app.tasks.organization.get_current_employee_task import GetCurrentEmployeeTask
from app.tasks.organization.get_organization_by_id_task import GetOrganizationByIdTask


class CreateRollCallUseCase:
    def __init__(self,
                 session: Annotated[sessionmaker, Depends(get_session)],
                 get_current_employee_task: Annotated[GetCurrentEmployeeTask, Depends(GetCurrentEmployeeTask)],
                 get_organization_by_id_task: Annotated[GetOrganizationByIdTask, Depends(GetOrganizationByIdTask)]
    ):
        self.session = session
        self.get_current_employee_task = get_current_employee_task
        self.get_organization_by_id_use_case = get_organization_by_id_task

    def execute(self, data: RollCallViewModel, user: User) -> RollCall:
        employee = self.get_current_employee_task.run(user)
        organization = self.get_organization_by_id_use_case.run(employee.organization_id)

        roll_call = RollCall(
            department_id=employee.department_id,
            employee_id=employee.id,
            organization_id=employee.organization_id,
            status=data.status,
            note=data.note
        )

        roll_call_location: Location | None = None
        sick_leave: SickLeave | None = None

        if data.location and data.location.lat and data.location.lng:
            roll_call_location = Location(
                lat=data.location.lat,
                lng=data.location.lng
            )

        if data.status == RollCallStatusEnum.ON_WORK:
            if ((employee.organization.location_lat and employee.organization.location_lng)
                    and data.location):
                distance = geopy.distance.geodesic(
                    (employee.organization.location_lat, employee.organization.location_lng),
                    (data.location.lat, data.location.lng)
                )
                if distance.m > 200:
                    raise HTTPException(
                        status_code=status.HTTP_400_BAD_REQUEST,
                        detail='You are not on the territory of the organization'
                    )
            if organization.settings and organization.settings.roll_call_end_time:
                now = datetime.now()
                roll_call_start_time_parsed = organization.settings.roll_call_end_time.split(':')
                roll_call_end_time = datetime(
                    now.year,
                    now.month,
                    now.day,
                    int(roll_call_start_time_parsed[0]),
                    int(roll_call_start_time_parsed[1])
                )
                if now > roll_call_end_time:
                    data.status = RollCallStatusEnum.LATE

        elif data.status == RollCallStatusEnum.OFF_DAY:
            today = date.today()
            if today.isoweekday() not in (6, 7): # Saturday and Sunday
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail='Today is not weekend'
                )
        elif data.status == RollCallStatusEnum.REASONED:
            roll_call.note = data.note
        elif data.status == RollCallStatusEnum.SICK:
            if not data.sick_leave:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail='Sick leave information doesn\'t sent'
                )
            sick_leave = SickLeave(
                note=data.note,
                date_from=data.sick_leave.date_from,
                date_to=data.sick_leave.date_to,
                employee_id=employee.id
            )

        with self.session() as session:
            session.add(roll_call)
            session.commit()
            session.refresh(roll_call)

            if roll_call_location:
                roll_call_location.roll_call_id = roll_call.id
                session.add(roll_call_location)
            if sick_leave:
                sick_leave.roll_call_id = roll_call.id
                session.add(sick_leave)
            session.commit()
            session.refresh(roll_call)

        return roll_call

