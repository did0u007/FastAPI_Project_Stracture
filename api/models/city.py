from sqlalchemy import Column, Integer, Unicode, ForeignKey
from api.models import *
from sqlalchemy.orm import relationship


class City(Base):
    __tablename__ = "cities"
    id = Column("id", Integer, primary_key=True, autoincrement=True)
    name = Column("name", Unicode, index=True, nullable=False)
    state_id = Column("states_id", Integer, ForeignKey("states.id"))
    state = relationship("State", foreign_keys=state_id)
