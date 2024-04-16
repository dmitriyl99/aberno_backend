from pydantic import BaseModel
from enum import Enum


class RollCallStatusEnum(str, Enum):
    ON_WORK = 'ON_WORK'
    OFF_DAY = 'OFF_DAY'
    SICK = 'SICK'
    REASONED = 'REASONED'


class RollCallViewModel(BaseModel):
    status: RollCallStatusEnum
    note: str | None = None
    organization_id: int
    department_id: int
