from sqlalchemy import Column, Integer, Unicode, ForeignKey
from api.models import Base
from sqlalchemy.orm import relationship


class City(Base):
    __tablename__ = "cities"
    id = Column("id", Integer, primary_key=True)
    name = Column("name", Unicode)
    state_id = Column("states_id", Integer, ForeignKey("states.id"))
    state = relationship("States", foreign_keys=state_id)
