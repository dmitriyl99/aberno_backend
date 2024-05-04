from enum import Enum
from datetime import date

from sqlalchemy import Integer, Date, String, Text, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .. import Base, TimestampMixin
from ..organization import Department, Employee


class TaskStatusEnum(Enum):
    PENDING = "PENDING"
    IN_PROGRESS = "IN_PROGRESS"
    COMPLETED = "COMPLETED"
    DELETED = "DELETED"


class TaskPriorityEnum(Enum):
    MEDIUM = "MEDIUM"
    HIGH = "HIGH"
    LOW = "LOW"


class Task(Base, TimestampMixin):
    __tablename__ = "tasks"

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(String(200))
    description: Mapped[str] = mapped_column(Text)
    status: Mapped[str] = mapped_column(String(50))
    priority: Mapped[str] = mapped_column(String(50))
    deadline: Mapped[date] = mapped_column(Date)

    department_id: Mapped[int] = mapped_column(ForeignKey('departments.id'))
    executor_id: Mapped[str] = mapped_column(ForeignKey('employees.id'))
    created_by_id: Mapped[int] = mapped_column(ForeignKey('employees.id'))

    department: Mapped[Department] = relationship(foreign_keys=[department_id])
    executor: Mapped[Employee] = relationship(foreign_keys=[executor_id])
    created_by: Mapped[Employee] = relationship(foreign_keys=[created_by_id])
