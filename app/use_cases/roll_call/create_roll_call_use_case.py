from typing import Annotated

from fastapi import Depends, HTTPException
from sqlalchemy import and_, cast, Date, or_
from sqlalchemy.orm import sessionmaker
import geopy.distance
from starlette import status

from datetime import date, datetime

from app.core.models.organization.schedule import ScheduleDay
from app.core.models.roll_call.sick_leave import SickLeave
from app.dal import get_session
from app.routers.admin.view_models import ScheduleDayEnum
from app.routers.roll_call.view_models import RollCallViewModel, RollCallStatusEnum
from app.core.models.roll_call.roll_call import RollCall, Location
from app.core.models.auth import User
from app.tasks.organization.get_current_employee_task import GetCurrentEmployeeTask
from app.tasks.organization.get_organization_by_id_task import GetOrganizationByIdTask
from app.use_cases.organization.department import GetDepartmentByIdUseCase


class CreateRollCallUseCase:
    def __init__(self,
                 session: Annotated[sessionmaker, Depends(get_session)],
                 get_current_employee_task: Annotated[GetCurrentEmployeeTask, Depends(GetCurrentEmployeeTask)],
                 get_organization_by_id_task: Annotated[GetOrganizationByIdTask, Depends(GetOrganizationByIdTask)],
                 get_department_by_id_use_case: Annotated[GetDepartmentByIdUseCase, Depends(GetDepartmentByIdUseCase)]
                 ):
        self.session = session
        self.get_current_employee_task = get_current_employee_task
        self.get_organization_by_id_use_case = get_organization_by_id_task
        self.get_department_by_id_use_case = get_department_by_id_use_case

    def execute(self, data: RollCallViewModel, user: User) -> RollCall:
        employee = self.get_current_employee_task.run(user)
        organization = self.get_organization_by_id_use_case.run(employee.organization_id)
        department = self.get_department_by_id_use_case.execute(employee.department_id)

        def get_current_schedule_day() -> ScheduleDay | None:
            if department.schedule:
                weekday = now.isoweekday()
                weekdays_mapper = {
                    1: ScheduleDayEnum.MONDAY,
                    2: ScheduleDayEnum.TUESDAY,
                    3: ScheduleDayEnum.WEDNESDAY,
                    4: ScheduleDayEnum.THURSDAY,
                    5: ScheduleDayEnum.FRIDAY,
                    6: ScheduleDayEnum.SATURDAY,
                    7: ScheduleDayEnum.SUNDAY
                }
                schedule_day: ScheduleDay = list(
                    filter(
                        lambda day: day.day == weekdays_mapper[weekday], department.schedule.days
                    )
                )[0]

                return schedule_day

            return None

        if (organization.settings and
                not organization.settings.work_leave_enabled and
                data.status == RollCallStatusEnum.LEAVE_WORK):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail='This status is not allowed in your organization'
            )
        if data.status != RollCallStatusEnum.LEAVE_WORK:
            with self.session() as session:
                today_roll_call = session.query(RollCall).filter(
                    and_(
                        RollCall.employee_id == employee.id,
                        cast(RollCall.created_at, Date) == date.today()
                    )
                ).first()
                if today_roll_call:
                    raise HTTPException(
                        status_code=status.HTTP_400_BAD_REQUEST,
                        detail="Today roll call already exists"
                    )
        if data.status == RollCallStatusEnum.LEAVE_WORK:
            with self.session() as session:
                today_on_work_roll_call = session.query(RollCall).filter(
                    and_(
                        RollCall.employee_id == employee.id,
                        cast(RollCall.created_at, Date) == date.today(),
                        or_(
                            RollCall.status == RollCallStatusEnum.ON_WORK.value,
                            RollCall.status == RollCallStatusEnum.LATE.value
                        )
                    )
                ).first()
                if not today_on_work_roll_call:
                    raise HTTPException(
                        status_code=status.HTTP_400_BAD_REQUEST,
                        detail="There is no record about on work today"
                    )

        roll_call_location: Location | None = None
        sick_leave: SickLeave | None = None
        now = datetime.now()

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
                if organization.settings and organization.settings.roll_call_distance:
                    if distance.m > organization.settings.roll_call_distance:
                        raise HTTPException(
                            status_code=status.HTTP_400_BAD_REQUEST,
                            detail='You are not on the territory of the organization'
                        )
            roll_call_end_time_parsed = ['11', '00']
            if organization.settings and organization.settings.roll_call_end_time:
                roll_call_end_time_parsed = organization.settings.roll_call_end_time.split(':')
            schedule_day = get_current_schedule_day()
            if schedule_day and schedule_day.roll_call_end_time:
                roll_call_end_time_parsed = schedule_day.roll_call_end_time.split(':')
            if roll_call_end_time_parsed:
                roll_call_end_time = datetime(
                    now.year,
                    now.month,
                    now.day,
                    int(roll_call_end_time_parsed[0]),
                    int(roll_call_end_time_parsed[1])
                )
                if now > roll_call_end_time:
                    data.status = RollCallStatusEnum.LATE

        elif data.status == RollCallStatusEnum.OFF_DAY:
            today = date.today()
            schedule_day = get_current_schedule_day()
            if schedule_day and not schedule_day.is_work_day:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail='Today is not weekend'
                )
            if not schedule_day and today.isoweekday() not in (6, 7):  # Saturday and Sunday
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail='Today is not weekend'
                )
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

        roll_call = RollCall(
            department_id=employee.department_id,
            employee_id=employee.id,
            organization_id=employee.organization_id,
            status=data.status,
            note=data.note
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
