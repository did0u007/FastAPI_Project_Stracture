from sqlalchemy import Column, Integer, Unicode
from api.models import *


class State(Base):
    __tablename__ = "states"
    id = Column("id", Integer, primary_key=True)
    name = Column("name", Unicode, unique=True, index=True, nullable=False)
