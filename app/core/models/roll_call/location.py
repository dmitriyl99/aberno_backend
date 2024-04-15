from .. import Base

from sqlalchemy import Float, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship


class Location(Base):
    __tablename__ = 'locations'

    id: Mapped[int] = mapped_column(primary_key=True)
    lat: Mapped[float] = mapped_column(Float)
    lng: Mapped[float] = mapped_column(Float)

    roll_call_id: Mapped[int] = mapped_column(ForeignKey('roll_calls.id'))

    roll_call: Mapped["RollCall"] = relationship(back_populates='location')
