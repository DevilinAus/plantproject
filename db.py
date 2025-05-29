import sqlite3
from config import DB_PATH


# could probably make a more robust function since a fair bit is reused here, where you can hand
# in the type of search.


def fetch(table, data_limit, column="date_time", order="DESC", select="*"):
    query = f"SELECT {select} FROM {table} ORDER BY {column} {order} LIMIT ?"

    # Reconnect to the DB
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute(query, (data_limit,))
    rows = cursor.fetchall()

    if select.strip().upper().startswith(("MIN(", "MAX(", "COUNT(", "AVG(", "SUM(")):
        return rows[0][0]

    # Close the connection
    connection.close()
    return rows


def fetch_latest(table, select="*"):
    query = f"SELECT {select} FROM {table}"

    # Reconnect to the DB
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute(query)
    row = cursor.fetchone()
    value = row[0]

    connection.close()
    return value


def get_connection():
    connection = sqlite3.connect(DB_PATH)
    connection.execute("PRAGMA journal_mode=WAL;")
    return connection


def fetch_between(table, newest_time, oldest_time):
    # query the raw db for every datapoint between the start and the end time
    connection = get_connection()
    cursor = connection.cursor()

    query = f"""
        SELECT * FROM {table}
        WHERE date_time BETWEEN ? AND ?
        ORDER BY date_time DESC
    """

    cursor.execute(query, (oldest_time, newest_time))
    rows = cursor.fetchall()
    print(f"Rows: {rows}")

    connection.close()
    return rows


# TODO return an OK or Error.
def store_data(timestamp, average_reading, table):
    # store that data with current date and hour (for label) in cleaned DB.
    connection = get_connection()
    cursor = connection.cursor()
    cursor.execute(
        """INSERT INTO avg_data (date_time, moisture_reading) 
                    VALUES (?, ?)
                    ON CONFLICT(date_time)
                    DO UPDATE SET moisture_reading = excluded.moisture_reading""",
        (timestamp, average_reading),
    )
    print(f"Wrote to DB -- TIMESTAMP: {timestamp} READING: {average_reading}")
    connection.commit()
    connection.close()


def store_weather(key, value):
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute(
        """
        INSERT INTO current_weather (key, value) 
        VALUES (?, ?)
        ON CONFLICT(key)
        DO UPDATE SET value = excluded.value""",
        (key, value),
    )

    connection.commit()
    connection.close()


def fetch_collected_at():
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("SELECT value FROM current_weather WHERE key = 'fetched_at'")
    result = cursor.fetchone()

    connection.close()

    result = result[0]

    return result


def fetch_all(table):
    connection = get_connection()
    cursor = connection.cursor()

    query = f"SELECT key, value FROM {table};"

    cursor.execute(query)
    results = cursor.fetchall()

    results = dict(results)

    return results
