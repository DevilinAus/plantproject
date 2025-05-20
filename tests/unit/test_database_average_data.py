from unittest.mock import Mock, ANY

from database_average_data import write_to_db


def describe_average_raw_data():
    def test_simple_mock(mocker):
        func = Mock()

        func(4, 4)
        func(4, 10)

        func.assert_called()
        func.assert_any_call(4, 10)
        func.assert_any_call(4, 4)
        # func.assert_not_called()

    def test_2():
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
        connection.execute.assert_any_call("PRAGMA journal_mode=WAL;")
        mock_cursor.execute.assert_any_call(ANY, (1, 1, 2))


# def do_stuff(connection):
#     connection.commit()
#     connection.close()
