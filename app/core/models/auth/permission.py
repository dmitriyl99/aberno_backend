from typing import List

from .. import Base
from .associations import roles_permissions
from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship


class Permission(Base):
    __tablename__ = "permissions"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(100), nullable=False)

    roles: Mapped[List["Role"]] = relationship(secondary=roles_permissions, back_populates='permissions')
