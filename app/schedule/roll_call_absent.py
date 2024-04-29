from datetime import datetime, timedelta

from sqlalchemy import and_

from app.dal import get_session
from app.core.models.roll_call.roll_call import RollCall
from app.core.models.organization import Organization, Employee
from app.routers.roll_call.view_models import RollCallStatusEnum


def roll_call_absent():
    now = datetime.utcnow() + timedelta(hours=5)
    now_start_day = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)

    with get_session()() as session:
        organizations = session.query(Organization).all()
        for organization in organizations:
            employees = session.query(Employee).filter(Employee.organization_id == organization.id).all()
            for employee in employees:
                roll_calls = session.query(RollCall).filter(and_(
                    RollCall.employee_id == employee.id,
                    RollCall.organization_id == employee.organization_id,
                    RollCall.created_at <= now,
                    RollCall.created_at >= now_start_day,
                ))
                if len(roll_calls) == 0:
                    session.add(RollCall(
                        department_id=employee.department_id,
                        employee_id=employee.id,
                        organization_id=employee.organization_id,
                        status=RollCallStatusEnum.ABSENT
                    ))

        session.commit()
