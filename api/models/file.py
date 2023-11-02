from sqlalchemy import Column, Integer, Unicode
from api.models import *


class File(Base):
    __tablename__ = "images"
    id = Column("id", Integer, primary_key=True)  # type: ignore
    url = Column("url", Unicode)
