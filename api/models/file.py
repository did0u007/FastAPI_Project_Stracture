from sqlalchemy import Column, Integer, Unicode
from api.models import Base


class File(Base):
    __tablename__ = "images"
    id = Column("id", Integer, primary_key=True)
    url = Column("url", Unicode)
