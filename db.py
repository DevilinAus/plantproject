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
