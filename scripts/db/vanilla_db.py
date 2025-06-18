from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Base

DATABASE_URL = "sqlite:///plant_info.db"

engine = create_engine(DATABASE_URL, echo=False)
SessionLocal = sessionmaker(bind=engine)


def override_database_for_testing(url: str):
    global engine, SessionLocal
    engine = create_engine(url, echo=False)
    SessionLocal = sessionmaker(bind=engine)
    Base.metadata.create_all(engine)
