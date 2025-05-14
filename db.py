import sqlite3
from config import DB_PATH


# could probably make a more robust function since a fair bit is reused here, where you can hand
# in the type of search.


def fetch(table, data_limit, column="date_time", order="DESC", select="*"):
    query = f"SELECT {select} FROM {table} ORDER BY {column} {order} LIMIT ?"

    # Reconnect to the DB
    connection = sqlite3.connect(DB_PATH)
    cursor = connection.cursor()

    cursor.execute(query, (data_limit,))
    rows = cursor.fetchall()

    if select.strip().upper().startswith(("MIN(", "MAX(", "COUNT(", "AVG(", "SUM(")):
        return rows[0][0]

    # Close the connection
    connection.close()
    return rows


def fetch_between(table, newest_time, oldest_time):
    # query the raw db for every datapoint between the start and the end time
    connection = sqlite3.connect(DB_PATH)
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
def store_data(timestamp, readable_text, average_reading, table):
    # store that data with current date and hour (for label) in cleaned DB.
    connection = sqlite3.connect(DB_PATH)
    cursor = connection.cursor()
    cursor.execute(
        """INSERT INTO avg_data (date_time, readable_text, moisture_reading) 
                    VALUES (?, ?, ?)
                    ON CONFLICT(date_time)
                    DO UPDATE SET moisture_reading = excluded.moisture_reading""",
        (timestamp, readable_text, average_reading),
    )
    print(
        f"Wrote to DB -- TIMESTAMP: {timestamp} READBLE: {readable_text}, READING: {average_reading}"
    )
    connection.commit()
    connection.close()
