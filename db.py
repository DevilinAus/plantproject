import sqlite3
from config import DB_PATH


# could probably make a more robust function since a fair bit is reused here, where you can hand
# in the type of search.


def fetch(table, data_limit):
    query = f"SELECT * FROM {table} ORDER BY date_time DESC LIMIT ?"

    # Reconnect to the DB
    connection = sqlite3.connect(DB_PATH)
    cursor = connection.cursor()

    cursor.execute(query, (data_limit,))
    rows = cursor.fetchall()

    # Close the connection
    connection.close()
    return rows


def fetch_between(start_time, end_time):
    # query the raw db for every datapoint between the start and the end time
    connection = sqlite3.connect(DB_PATH)
    cursor = connection.cursor()

    cursor.execute(
        "SELECT * FROM minute_reading WHERE date_time BETWEEN ? AND ? ORDER BY date_time DESC",
        (start_time, end_time),
    )
    rows = cursor.fetchall()
    print(rows)

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
