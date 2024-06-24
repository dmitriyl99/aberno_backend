from typing import List
from enum import Enum
from datetime import datetime

from sqlalchemy import String, Text, ForeignKey, Boolean, DateTime, Integer, Table, Column
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


class EmployeesTasks(Base):
    __tablename__ = "employees_tasks"
    employee_id: Mapped[int] = mapped_column(ForeignKey('employees.id'), primary_key=True)
    task_id: Mapped[int] = mapped_column(ForeignKey('tasks.id'), primary_key=True)
    status: Mapped[str] = mapped_column(String(100))
    viewed: Mapped[bool] = mapped_column(Boolean(), default=False)
    viewed_at: Mapped[datetime] = mapped_column(DateTime, nullable=True)
    employee: Mapped[Employee] = relationship()


controller_task_table = Table(
    "controller_task",
    Base.metadata,
    Column("task_id", Integer, ForeignKey('tasks.id', ondelete='CASCADE')),
    Column("employee_id", Integer, ForeignKey('employees.id', ondelete='CASCADE'))
)


class TaskComment(Base):
    __tablename__ = "task_comments"

    id: Mapped[int] = mapped_column(primary_key=True)
    task_id: Mapped[int] = mapped_column(Integer, ForeignKey('tasks.id', ondelete='CASCADE'), nullable=False)
    employee_id: Mapped[int] = mapped_column(Integer, ForeignKey('employees.id', ondelete='SET NULL'), nullable=True)
    text: Mapped[str] = mapped_column(Text)

    employee: Mapped[Employee] = relationship(foreign_keys=[employee_id])


class Task(Base, TimestampMixin):
    __tablename__ = "tasks"

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(String(200))
    description: Mapped[str] = mapped_column(Text)
    status: Mapped[str] = mapped_column(String(100))
    priority: Mapped[str] = mapped_column(String(50))
    deadline: Mapped[datetime] = mapped_column(DateTime, nullable=True)
    deadline_end: Mapped[datetime] = mapped_column(DateTime, nullable=True)

    department_id: Mapped[int] = mapped_column(ForeignKey('departments.id'))
    created_by_id: Mapped[int] = mapped_column(ForeignKey('employees.id'))
    organization_id: Mapped[int] = mapped_column(ForeignKey('organizations.id'))

    department: Mapped[Department] = relationship(foreign_keys=[department_id])
    executors: Mapped[List[EmployeesTasks]] = relationship()
    created_by: Mapped[Employee] = relationship(foreign_keys=[created_by_id])
    controllers: Mapped[List[Employee]] = relationship(secondary=controller_task_table)
    comments: Mapped[List[TaskComment]] = relationship()
