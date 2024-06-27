from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool
from app.data.database import Base
from functools import lru_cache


# needs to be cached so all calls to get_engine return the same engine
@lru_cache
def get_engine():
    SQLALCHEMY_DATABASE_URL = "sqlite://"
    return create_engine(
        SQLALCHEMY_DATABASE_URL,
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )


def set_up_db():
    Base.metadata.create_all(bind=get_engine())


def clean_up_db():
    Base.metadata.drop_all(bind=get_engine())


def get_session():
    return sessionmaker(autocommit=False, autoflush=False, bind=get_engine())()
