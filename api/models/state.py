from sqlalchemy import Column, Integer, Unicode
from api.models import *
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column as Column


class State(Base):
    __tablename__ = "states"
    id: Mapped[int] = Column(primary_key=True, autoincrement="auto")
    name: Mapped[str] = Column(unique=True, index=True, nullable=False)
