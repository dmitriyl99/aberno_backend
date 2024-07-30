import datetime
from typing import Annotated, List

from fastapi import Depends
from sqlalchemy.orm import sessionmaker, joinedload

from app.core.models.organization import Employee
from app.core.models.organization.schedule import Schedule, ScheduleDay
from app.dal import get_session
from app.routers.admin.view_models import ScheduleDayViewModel


class CreateEmployeeScheduleUseCase:
    def __init__(self,
                 session: Annotated[sessionmaker, Depends(get_session)],
                 ):
        self.session = session

    def execute(self, employee_id: int, days: List[ScheduleDayViewModel]) -> List[ScheduleDay]:
        with self.session() as session:
            employee: Employee = session.query(Employee).options(
                joinedload(Employee.schedule).joinedload(Schedule.days)
            ).get(employee_id)
            schedule = employee.schedule
            if not schedule:
                schedule = Schedule(employee_id=employee_id)
            schedule.updated_at = datetime.datetime.now()
            result_days = []
            for day in days:
                schedule_days = list(
                    filter(
                        lambda d: d.day == day.day, schedule.days
                    )
                )
                if len(schedule_days) == 0:
                    schedule_day = ScheduleDay(day=day.day)
                    schedule.days.append(schedule_day)
                else:
                    schedule_day = schedule_days[0]
                schedule_day.work_start_time = day.work_start_time,
                schedule_day.work_end_time = day.work_end_time,
                schedule_day.roll_call_start_time = day.roll_call_start_time,
                schedule_day.roll_call_end_time = day.roll_call_end_time
                schedule_day.is_work_day = day.is_work_day
                result_days.append(schedule_day)
            session.add(schedule)
            session.commit()
            session.refresh(schedule)
            employee.schedule_id = schedule.id
            session.commit()

            for result_day in result_days:
                session.refresh(result_day)

            return result_days
