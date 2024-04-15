from typing import List

from sqlalchemy import Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .. import Base
from app.core.models import TimestampMixin


class Organization(Base, TimestampMixin):
    __tablename__ = "organizations"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(Text)
    legal_name: Mapped[str] = mapped_column(Text)
    legal_name_prefix: Mapped[str] = mapped_column(Text)

    departments: Mapped[List["Department"]] = relationship(back_populates='organization')
    employees: Mapped[List["Employee"]] = relationship(back_populates='organization')
