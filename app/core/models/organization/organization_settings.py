from .. import Base

from sqlalchemy import Integer, String, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column


class OrganizationSettings(Base):
    __tablename__ = "organization_settings"

    id: Mapped[int] = mapped_column(primary_key=True)
    organization_id: Mapped[int] = mapped_column(ForeignKey('organizations.id'))

    roll_call_start_time: Mapped[str] = mapped_column(String(5))
    roll_call_end_time: Mapped[str] = mapped_column(String(5))
