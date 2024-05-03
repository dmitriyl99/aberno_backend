from typing import List

from .. import Base, TimestampMixin

from sqlalchemy import Integer, ForeignKey, String, Boolean
from sqlalchemy.orm import Mapped, mapped_column, relationship


class Schedule(TimestampMixin, Base):
    __tablename__ = 'schedules'

    id: Mapped[int] = mapped_column(primary_key=True)
    department_id: Mapped[int] = mapped_column(ForeignKey('departments.id'))

    days: Mapped[List["ScheduleDay"]] = relationship()


class ScheduleDay(TimestampMixin, Base):
    __tablename__ = 'schedule_days'

    id: Mapped[int] = mapped_column(primary_key=True)
    day: Mapped[str] = mapped_column(String(20))
    is_work_day: Mapped[bool] = mapped_column(Boolean)
    work_start_time: Mapped[str] = mapped_column(String(5))
    work_end_time: Mapped[str] = mapped_column(String(5))
    roll_call_start_time: Mapped[str] = mapped_column(String(5))
    roll_call_end_time: Mapped[str] = mapped_column(String(5))
    schedule_id: Mapped[int] = mapped_column(ForeignKey('schedules.id'))
