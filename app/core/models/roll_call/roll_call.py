from .location import Location
from .sick_leave import SickLeave
from .. import Base, TimestampMixin

from enum import Enum as NativeEnum

from sqlalchemy import Enum, ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship


class RollCallStatusEnum(str, NativeEnum):
    ON_WORK = 'ON_WORK'
    OFF_DAY = 'OFF_DAY'
    LATE = 'LATE'
    SICK = 'SICK'
    ABSENT = 'ABSENT'
    REASONED = 'REASONED'
    LEAVE_WORK = 'LEAVE_WORK'


class RollCall(Base, TimestampMixin):
    __tablename__ = 'roll_calls'

    id: Mapped[int] = mapped_column(primary_key=True)
    status: Mapped[str] = mapped_column(Enum(
        'ON_WORK', 'OFF_DAY', 'SICK', 'REASONED', 'LEAVE_WORK', 'LATE', 'ABSENT'), name='status')
    note: Mapped[str] = mapped_column(String)

    employee_id: Mapped[int] = mapped_column(ForeignKey('employees.id'))
    organization_id: Mapped[int] = mapped_column(ForeignKey('organizations.id'))
    department_id: Mapped[int] = mapped_column(ForeignKey("departments.id"))

    employee: Mapped["Employee"] = relationship(back_populates='roll_calls')
    organization: Mapped["Organization"] = relationship()
    department: Mapped["Department"] = relationship()
    location: Mapped["Location"] = relationship(back_populates='roll_call')
    sick_leave: Mapped["SickLeave"] = relationship("SickLeave")
