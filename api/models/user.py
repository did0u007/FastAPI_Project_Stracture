from sqlalchemy.orm import mapped_column as Column
from sqlalchemy.orm import relationship, Mapped
from api.core.enums import UserType
from sqlalchemy import ForeignKey
from api.models import *
from typing import Optional
import datetime as dt


class User(Base):
    __tablename__ = "users"
    id: Mapped[int] = Column(primary_key=True, autoincrement="auto")
    name: Mapped[Optional[str]] = Column(index=True, nullable=True)
    username: Mapped[str] = Column(index=True)
    email: Mapped[str] = Column(unique=True, index=True)
    password: Mapped[str] = Column()
    profile_img: Mapped[Optional[int]] = Column(ForeignKey("images.id"), nullable=True)
    remember_token: Mapped[str] = Column()
    user_type: Mapped[UserType] = Column(default=UserType.USER, nullable=False)
    city_id: Mapped[Optional[int]] = Column(ForeignKey("cities.id"), nullable=True)
    state_id: Mapped[int] = Column(ForeignKey("states.id"))
    address: Mapped[str] = Column()
    phone: Mapped[str] = Column(unique=True)
    deleted_at: Mapped[dt.datetime] = Column(default=None)
    created_at: Mapped[dt.datetime] = Column(default=lambda: dt.datetime.now(dt.UTC))
    updated_at: Mapped[dt.datetime] = Column(default=None)

    Cities = relationship("City", foreign_keys=city_id)
    States = relationship("State", foreign_keys=state_id)
    Images = relationship("File", foreign_keys=profile_img)
