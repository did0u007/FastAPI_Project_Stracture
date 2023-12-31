from sqlalchemy import Unicode
from api.models import *
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column as Column


class File(Base):
    __tablename__ = "images"
    id: Mapped[int] = Column(primary_key=True, autoincrement="auto")  # type: ignore
    path: Mapped[str] = Column(Unicode(255), nullable=False)
    file_name: Mapped[str] = Column(
        Unicode(50), unique=True, nullable=False, index=True
    )
