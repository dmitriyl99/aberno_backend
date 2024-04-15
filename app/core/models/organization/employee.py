from datetime import date

from sqlalchemy import Date, String, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .. import Base
from app.core.models import TimestampMixin
from app.core.models.auth.user import User
from app.core.models.organization.organization import Organization
from app.core.models.organization.department import Department


class Employee(Base, TimestampMixin):
    __tablename__ = "employees"
    id: Mapped[int] = mapped_column(primary_key=True)
    birth_date: Mapped[date] = mapped_column(Date)
    phone: Mapped[str] = mapped_column(String(12))

    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    organization_id: Mapped[int] = mapped_column(ForeignKey("organizations.id"))
    department_id: Mapped[int] = mapped_column(ForeignKey("departments.id"))

    user: Mapped["User"] = relationship(back_populates='employee')
    organization: Mapped["Organization"] = relationship(back_populates='employees')
    department: Mapped["Department"] = relationship(related_name='employees')