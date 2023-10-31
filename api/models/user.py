from sqlalchemy import Column, Enum, ForeignKey, Integer, Time, Unicode
from api.models import Base
from api.core.enums import userType
from sqlalchemy.orm import relationship


class User(Base):
    __tablename__ = "users"
    id = Column("id", Integer, primary_key=True)
    name = Column("name", Unicode)
    username = Column("username", Unicode)
    email = Column("email", Unicode)
    password = Column("password", Unicode)
    profile_img = Column("profile_img", Integer, ForeignKey("images.id"))
    remember_token = Column("remember_token", Unicode)
    user_type = Column("user_type", Enum(userType), default=userType.USER)
    cities_id = Column("cities_id", Integer, ForeignKey("cities.id"))
    states_id = Column("states_id", Integer, ForeignKey("states.id"))
    address = Column("address", Unicode)
    phone = Column("phone", Unicode)
    deleted_at = Column("deleted_at", Time)
    created_at = Column("created_at", Time)
    updated_at = Column("updated_at", Time)

    cities = relationship("Cities", foreign_keys=cities_id)
    states = relationship("States", foreign_keys=states_id)
    images = relationship("Images", foreign_keys=profile_img)
