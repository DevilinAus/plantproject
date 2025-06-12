import pytest
from app import create_app
from models.database import SessionLocal
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


@pytest.fixture()
def app():
    app = create_app(
        {
            "TESTING": True,
            "SQLALCHEMY_DATABASE_URI": "sqlite:///:memory:",
        }
    )

    # Activate app context for the entire test duration
    with app.app_context():
        # Initialize fresh database
        db.create_all()

        # Make app available for tests
        yield app

        # Cleanup
        db.drop_all()


@pytest.fixture
def client(app):
    return app.test_client()


@pytest.fixture
def runner(app):
    return app.test_cli_runner()


@pytest.fixture
def db_session():
    db.session.begin_nested()  # Start savepoint for rollback

    yield db.session

    db.session.rollback()  # Rollback to savepoint
    db.session.close()


@pytest.fixture
def seed_database(decoupled_session):
    from database_average_data import Base, RawData

    engine, Session = decoupled_session
    Base.metadata.create_all(engine)

    seed_data = [
        # Hour 1 (3 timestamps)
        (1686495605, 0),
        (1686495623, 0),
        (1686495734, 0),
        # Hour 2 (4 timestamps)
        (1686499202, 0),
        (1686499322, 0),
        (1686499387, 0),
        (1686499455, 0),
        # Hour 3 (0 timestamps, for testing Null)
        # Hour 4 (6 timestamps)
        (1686506401, 0),
        (1686506456, 0),
        (1686506550, 0),
        (1686506599, 0),
        (1686506690, 0),
        (1686506733, 0),
        # Hour 5 (3 timestamps)
        (1686510004, 0),
        (1686510075, 0),
        (1686510099, 0),
        # Hour 6 (8 timestamps)
        (1686513600, 0),
        (1686513632, 0),
        (1686513701, 0),
        (1686513750, 0),
        (1686513799, 0),
        (1686513822, 0),
        (1686513850, 0),
        (1686513888, 0),
    ]

    with Session() as session:
        for timestamp, value in seed_data:
            session.add(RawData(timestamp=timestamp, value=value))
            session.commit()

    return engine, Session


@pytest.fixture
def decoupled_session():
    engine = create_engine("sqlite:///:memory:", future=True)
    Session = sessionmaker(bind=engine, future=True)
    return engine, Session
