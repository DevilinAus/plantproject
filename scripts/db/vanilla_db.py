from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Base

DATABASE_URI = "sqlite:///instance/plant_info.db"


def get_engine_and_session(database_uri=DATABASE_URI):
    engine = create_engine(database_uri, echo=False, future=True)
    SessionLocal = sessionmaker(bind=engine)
    Base.metadata.create_all(engine)
    return engine, SessionLocal
