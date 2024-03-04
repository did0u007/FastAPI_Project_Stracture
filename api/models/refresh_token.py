from sqlalchemy import Integer, ForeignKey, UnicodeText
from sqlalchemy.orm import Mapped, relationship
from sqlalchemy.orm import mapped_column as Column

from api.models import *


class RefreshToken(Base):
    __tablename__ = "refresh_tokens"
    #
    id: Mapped[int] = Column(Integer, primary_key=True, autoincrement="auto")
    user_id: Mapped[int] = Column(Integer, ForeignKey("users.id"), unique=Truesudo nala)  # type: ignore
    token: Mapped[str] = Column(UnicodeText, nullable=False, unique=True)
    #
    user = relationship("User", foreign_keys=user_id)
