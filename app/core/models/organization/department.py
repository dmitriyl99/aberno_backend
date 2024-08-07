from typing import List

from sqlalchemy import Text, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .schedule import Schedule
from .. import Base
from app.core.models import TimestampMixin


class Department(Base, TimestampMixin):
    __tablename__ = "departments"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(Text)
    organization_id: Mapped[int] = mapped_column(ForeignKey("organizations.id"))
    schedule_id: Mapped[int] = mapped_column(ForeignKey("schedules.id", ondelete='CASCADE'))

    organization: Mapped["Organization"] = relationship(back_populates='departments')
    employees: Mapped[List["Employee"]] = relationship(back_populates='department')

    schedule: Mapped["Schedule"] = relationship(foreign_keys=[schedule_id])
