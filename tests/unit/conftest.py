import pytest
from app import create_app
from app.db.database import db


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
