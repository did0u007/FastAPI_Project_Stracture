from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import MappedAsDataclass, DeclarativeBase
from sqlalchemy.ext.declarative import declarative_base

DATABASE_URL = "sqlite:///api/db/database.sqlite"  # should be came from core.setting [using .env file]
engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False},
    pool_pre_ping=True,
    pool_recycle=300,
    pool_size=5,
    max_overflow=0,
)
sessionLocal = sessionmaker(autoflush=False, autocommit=False, bind=engine)


class Base(DeclarativeBase):
    pass


# Base = declarative_base()


def get_db():
    db = sessionLocal()
    try:
        yield db
    finally:
        db.close()
