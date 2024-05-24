from datetime import datetime, timedelta

from sqlalchemy import and_

from app.core.models.organization.schedule import ScheduleDay
from app.dal import get_session
from app.core.models.roll_call.roll_call import RollCall, RollCallStatusEnum
from app.core.models.organization import Organization, Employee
from app.core.models.organization.department import Schedule
from app.routers.admin.view_models import ScheduleDayEnum


def roll_call_absent():
    now = datetime.utcnow() + timedelta(hours=5)
    now_start_day = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
    weekdays_mapper = {
        1: ScheduleDayEnum.MONDAY,
        2: ScheduleDayEnum.TUESDAY,
        3: ScheduleDayEnum.WEDNESDAY,
        4: ScheduleDayEnum.THURSDAY,
        5: ScheduleDayEnum.FRIDAY,
        6: ScheduleDayEnum.SATURDAY,
        7: ScheduleDayEnum.SUNDAY
    }

    with get_session()() as session:
        organizations = session.query(Organization).all()
        departments_schedules = {}
        for organization in organizations:
            employees = session.query(Employee).filter(Employee.organization_id == organization.id).all()
            for employee in employees:
                roll_calls = session.query(RollCall).filter(and_(
                    RollCall.employee_id == employee.id,
                    RollCall.organization_id == employee.organization_id,
                    RollCall.created_at <= now,
                    RollCall.created_at >= now_start_day,
                )).all()
                if len(roll_calls) == 0:
                    if employee.department_id in departments_schedules:
                        schedules = departments_schedules[employee.department_id]
                    else:
                        schedules = session.query(Schedule).filter(
                            Schedule.department_id == employee.department_id).all()
                        departments_schedules[employee.department_id] = schedules
                    weekday = now.isoweekday()
                    schedule_days = list(
                        filter(
                            lambda day: day.day == weekdays_mapper[weekday], schedules
                        )
                    )
                    status = RollCallStatusEnum.ABSENT.value
                    if len(schedule_days) > 0:
                        schedule_day: ScheduleDay = schedule_days[0]
                        if not schedule_day.is_work_day:
                            status = RollCallStatusEnum.OFF_DAY.value
                    session.add(RollCall(
                        department_id=employee.department_id,
                        employee_id=employee.id,
                        organization_id=employee.organization_id,
                        status=status
                    ))

        session.commit()
