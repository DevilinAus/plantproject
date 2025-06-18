from unittest.mock import Mock, ANY
from app.db.flask_db import db
from models.models import RawData
from scripts.db.vanilla_db import SessionLocal


from app import create_app
from sqlalchemy import select

from database_average_data import (
    round_down_to_hour,
    Session,
    create_engine,
)


def describe_average_raw_data():
    def test_round_down_to_hour():
        returned_ts = round_down_to_hour(1754913805)
        assert returned_ts == 1754913600

    def test_start_time():
        pass

    def test_oldest_query(seed_database):
        engine, Session = seed_database
        session = SessionLocal()

        oldest_timestamp = session.execute(
            select(RawData.timestamp).order_by(RawData.timestamp.asc()).limit(1)
        ).scalar_one()
        assert oldest_timestamp == 1686495605

    # average_raw_data_loop
    # patch start_time & oldest query.
    # seed test data into the in-memory database.

    def test_simple_mock(mocker):
        func = Mock()

        func(4, 4)
        func(4, 10)

        func.assert_called()
        func.assert_any_call(4, 10)
        func.assert_any_call(4, 4)
        # func.assert_not_called()


def disabled_test_2():
    # TODO Needs to be rewritten to work with new ORM.
    mock_cursor = Mock()

    def get_mock_cursor():
        return mock_cursor

    connection = Mock()
    connection.cursor = get_mock_cursor

    # connection.close()

    # Do some stuff with connection
    write_to_db(1, 2, connection)

    connection.close.assert_called()
    connection.commit.assert_called()
    mock_cursor.execute.assert_any_call(ANY, (1, 2))
