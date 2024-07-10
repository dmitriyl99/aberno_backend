from datetime import date
from typing import List

from sqlalchemy import Date, String, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .position import Position
from .. import Base
from app.core.models import TimestampMixin
from app.core.models.auth.user import User
from app.core.models.organization.organization import Organization
from app.core.models.organization.department import Department
from ..roll_call.roll_call import RollCall


class Employee(Base, TimestampMixin):
    __tablename__ = "employees"
    id: Mapped[int] = mapped_column(primary_key=True)
    phone: Mapped[str] = mapped_column(String(12))

    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    organization_id: Mapped[int] = mapped_column(ForeignKey("organizations.id"))
    department_id: Mapped[int] = mapped_column(ForeignKey("departments.id", ondelete='CASCADE'))
    created_by_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    position_id: Mapped[int] = mapped_column(ForeignKey("positions.id"))

    user: Mapped["User"] = relationship(foreign_keys=[user_id])
    organization: Mapped["Organization"] = relationship(back_populates='employees')
    department: Mapped["Department"] = relationship(back_populates='employees')
    position: Mapped["Position"] = relationship(foreign_keys=[])
    roll_calls: Mapped[List["RollCall"]] = relationship(back_populates='employee')
    created_by: Mapped["User"] = relationship(foreign_keys=[created_by_id])
