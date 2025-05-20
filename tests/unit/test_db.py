from unittest.mock import Mock


from db import get_connection


def disabled_test_get_connection_test(mocker):
    # Arrange (setup)
    mock_connection = Mock()
    mock_sqlite3_connect = mocker.patch("sqlite3.connect", return_value=mock_connection)

    # act
    connection = get_connection()

    # assert
    # something broke here with assertions.
    mock_sqlite3_connect.assert_called("DB_PATH")
    mock_connection.execute.assert_called("PRAGMA journal_mode=WAL;")

    assert connection == mock_connection

    # #  db.py understanding
    # connection (object)
    # sqlite3 (object)
    #     connect (function)

    # DB_path = variable

    # mock.anything

    # mock(test)
