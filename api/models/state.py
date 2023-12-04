from typing import List
from sqlalchemy import Column, Unicode
from api.models import *
from sqlalchemy.orm import Mapped, relationship
from sqlalchemy.orm import mapped_column as Column


class State(Base):
    __tablename__ = "states"
    #
    id: Mapped[int] = Column(primary_key=True, autoincrement="auto")
    name: Mapped[str] = Column(Unicode(50), unique=True, index=True, nullable=False)
    #
    cities = relationship("City", back_populates="state", cascade="delete, all")
