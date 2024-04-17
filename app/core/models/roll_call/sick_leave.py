from .. import Base, TimestampMixin
from sqlalchemy import Integer, String, Date, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

from datetime import date


class SickLeave(Base, TimestampMixin):
    __tablename__ = "sick_leave"

    id: Mapped[int] = mapped_column(primary_key=True)
    note: Mapped[str] = mapped_column(String(200))
    date_from: Mapped[date] = mapped_column(Date)
    date_to: Mapped[date] = mapped_column(Date)

    employee_id: Mapped[int] = mapped_column(ForeignKey("employees.id"))
    roll_call_id: Mapped[int] = mapped_column(ForeignKey("roll_calls.id"))
