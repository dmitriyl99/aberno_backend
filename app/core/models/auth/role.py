from typing import List

from .. import Base
from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship
from .associations import roles_permissions


class Role(Base):

    __tablename__ = "roles"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(100))

    permissions: Mapped[List["Permission"]] = relationship(secondary=roles_permissions, back_populates='roles')
