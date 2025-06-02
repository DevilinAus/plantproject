import pytest
from app import create_app
from app.db.database import db


@pytest.fixture(scope="module")
def app():
    app = create_app(
        {
            "TESTING": True,
            "SQLALCHEMY_DATABASE_URI": "sqlite:///:memory:",
        }
    )

    ctx = app.app_context()
    ctx.push()

    db.create_all()
    yield app
    db.drop_all()
    ctx.pop()


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
