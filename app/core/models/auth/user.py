from typing import List

from .. import Base
from sqlalchemy import String, Text, Boolean
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
    username: Mapped[str] = mapped_column(String(100), nullable=True)
    password: Mapped[str] = mapped_column(Text)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    firebase_notification_token: Mapped[str] = mapped_column(Text, nullable=True)
    employee_number: Mapped[str] = mapped_column(String(100), nullable=True)

    roles: Mapped[List[Role]] = relationship(secondary=roles_users)
    permissions: Mapped[List[Permission]] = relationship(secondary=permissions_users)

    @property
    def is_admin(self) -> bool:
        return len(
            list(
                filter(
                    lambda r: r.name == 'Admin', self.roles
                )
            )
        ) > 0

    @property
    def is_super_admin(self) -> bool:
        return len(
            list(
                filter(
                    lambda r: r.name == 'Super Admin', self.roles
                )
            )
        ) > 0
