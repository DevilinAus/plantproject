from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

Base = declarative_base()

engine = None
SessionLocal = None


def init_db(db_url):
    global engine, SessionLocal
    engine = create_engine(db_url, echo=True, future=True)
    SessionLocal = sessionmaker(
        bind=engine, autoflush=False, autocommit=False, future=True
    )
    Base.metadata.create_all(bind=engine)
