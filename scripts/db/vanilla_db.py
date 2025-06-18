from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Base

DATABASE_URL = "sqlite:///plant_info.db"


def get_engine_and_session(database_url=DATABASE_URL):
    engine = create_engine(database_url, echo=False)
    SessionLocal = sessionmaker(bind=engine)
    Base.metadata.create_all(engine)
    return engine, SessionLocal
