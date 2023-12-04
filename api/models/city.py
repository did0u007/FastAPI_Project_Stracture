from sqlalchemy.orm import relationship, Mapped
from sqlalchemy.orm import mapped_column as Column
from sqlalchemy import ForeignKey, Unicode
from api.models import *


class City(Base):
    __tablename__ = "cities"
    #
    id: Mapped[int] = Column(primary_key=True, autoincrement="auto")
    name: Mapped[str] = Column(Unicode(50), index=True, nullable=False)
    state_id: Mapped[int] = Column(
        ForeignKey("states.id", ondelete="CASCADE"), nullable=False
    )
    #
    state = relationship("State", back_populates="cities")
