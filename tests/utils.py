from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool
from app.data.database import Base
from sqlalchemy.sql import text
import csv
import datetime
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
    # add data to the table from sunrise_sunset.csv
    session = get_session()
    with open("alembic/versions/sunrise_sunset.csv") as f:
        reader = csv.reader(f)
        next(reader)
        for index, row in enumerate(reader):
            id = index
            month = row[0]
            day = row[1]
            sunrise = datetime.datetime.strptime(row[2].split("+")[0], "%Y-%m-%d %H:%M:%S")
            sunset = datetime.datetime.strptime(row[3].split("+")[0], "%Y-%m-%d %H:%M:%S")
            city = row[4]
            session.execute(
                text(f"INSERT INTO sunset_sunrise (id, month, day, sunrise, sunset, city) VALUES ({id}, {month}, {day}, '{sunrise}', '{sunset}', '{city}')")
            )


def clean_up_db():
    Base.metadata.drop_all(bind=get_engine())


def get_session():
    return sessionmaker(autocommit=False, autoflush=False, bind=get_engine())()
