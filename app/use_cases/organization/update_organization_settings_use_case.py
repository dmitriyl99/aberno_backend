from typing import Annotated

from fastapi import Depends
from sqlalchemy.orm import sessionmaker

from app.core.models.auth import User
from app.core.models.organization.organization_settings import OrganizationSettings
from app.dal import get_session
from app.routers.admin.view_models import OrganizationSettingsViewModel
from app.tasks.organization.get_current_employee_task import GetCurrentEmployeeTask


class UpdateOrganizationSettingsUseCase:
    def __init__(self,
                 session: Annotated[sessionmaker, Depends(get_session)],
                 get_current_employee_task: Annotated[GetCurrentEmployeeTask, Depends(GetCurrentEmployeeTask)]
                 ):
        self.session = session
        self.get_current_employee_task = get_current_employee_task

    def execute(self, user: User, data: OrganizationSettingsViewModel) -> OrganizationSettings:
        employee = self.get_current_employee_task.run(user)
        with self.session() as session:
            settings = session.query(OrganizationSettings).filter(
                OrganizationSettings.organization_id == employee.organization_id
            ).first()
            if not settings:
                settings = OrganizationSettings()
                settings.organization_id = employee.organization_id
            settings.roll_call_start_time = data.roll_call_start_time
            settings.roll_call_end_time = data.roll_call_end_time
            settings.roll_call_distance = data.roll_call_distance
            settings.work_leave_enabled = data.work_leave_enabled
            session.add(settings)
            session.commit()
            session.refresh(settings)
        return settings
