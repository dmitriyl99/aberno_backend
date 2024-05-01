from typing import List

from .. import Base
from sqlalchemy import String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship
from .associations import roles_users, permissions_users

from app.core.models import TimestampMixin
from app.core.models.auth.permission import Permission
from app.core.models.auth.role import Role


class User(Base, TimestampMixin):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(200))
    last_name: Mapped[str] = mapped_column(String(200))
    username: Mapped[str] = mapped_column(String(100))
    password: Mapped[str] = mapped_column(Text)

    roles: Mapped[List[Role]] = relationship(secondary=roles_users)
    permissions: Mapped[List[Permission]] = relationship(secondary=permissions_users)
