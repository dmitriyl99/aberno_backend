import datetime
from typing import Annotated, List

from fastapi import Depends
from sqlalchemy.orm import sessionmaker, joinedload

from app.core.models.organization import Department
from app.core.models.organization.schedule import Schedule, ScheduleDay
from app.dal import get_session
from app.routers.admin.view_models import ScheduleDayViewModel


class CreateDepartmentScheduleUseCase:
    def __init__(self,
                 session: Annotated[sessionmaker, Depends(get_session)],
                 ):
        self.session = session

    def execute(self, department_id: int, days: List[ScheduleDayViewModel]) -> Schedule:
        with self.session() as session:
            department: Department = session.query(Department).options(
                joinedload(Department.schedule).joinedload(Schedule.days)
            ).get(department_id)
            schedule = department.schedule
            if not schedule:
                schedule = Schedule(department_id=department_id)
            schedule.updated_at = datetime.datetime.now()
            for day in days:
                schedule_days = list(
                    filter(
                        lambda d: d.day == day.day, schedule.days
                    )
                )
                if len(schedule_days) == 0:
                    schedule_day = ScheduleDay(day=day)
                    schedule.days.append(schedule_day)
                else:
                    schedule_day = schedule_days[0]
                schedule_day.work_start_time = day.work_start_time,
                schedule_day.work_end_time = day.work_end_time,
                schedule_day.roll_call_start_time = day.roll_call_start_time,
                schedule_day.roll_call_end_time = day.roll_call_end_time
                schedule_day.is_work_day = day.is_work_day
            session.add(schedule)
            session.commit()
            session.refresh(schedule)
            session.refresh(schedule.days)

            return schedule
