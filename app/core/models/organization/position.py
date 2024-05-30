from sqlalchemy import String, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

from .. import Base


class Position(Base):
    __tablename__ = "positions"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(200))

    organization_id: Mapped[int] = mapped_column(ForeignKey('organizations.id'))
