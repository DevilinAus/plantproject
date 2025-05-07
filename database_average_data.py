import sqlite3
import datetime
from datetime import timedelta


# TODO make this function scaleable - it would be good if it could be passed in the hour so it
# could loop over hours gone.
def average_raw_data():
    # this should be triggered every hour.

    # get current timestamp (end?)
    now = datetime.datetime.now()
    rounded_now = now.replace(minute=0, second=0, microsecond=0)

    # work out what timestamp it was an hour ago(start)
    one_hour_ago = rounded_now - timedelta(hours=1)

    # convert times to database friendly timestamps
    now_timestamp = rounded_now.timestamp()
    one_hour_ago_timestamp = one_hour_ago.timestamp()

    # figure out what the hour is in local time
    this_hour = rounded_now.hour

    print(this_hour)

    # query the raw db for every datapoint between the start and the end time
    connection = sqlite3.connect("plant_info.db")
    cursor = connection.cursor()

    cursor.execute(
        "SELECT * FROM minute_reading WHERE date_time BETWEEN ? AND ? ORDER BY date_time DESC",
        (one_hour_ago_timestamp, now_timestamp),
    )
    rows = cursor.fetchall()
    print(rows)

    connection.close()

    # count how many data points
    reading_count = 0
    total_reading_value = 0

    for row in rows:
        reading_count += 1
        total_reading_value += row[1]

    print(reading_count)
    print(total_reading_value)

    # add data up & divide by count (get average)
    if reading_count > 0:
        average_reading = round(total_reading_value / reading_count)
    else:
        average_reading = None

    print(average_reading)

    # store that data with current date and hour (for label) in cleaned DB.
    connection = sqlite3.connect("plant_info.db")
    cursor = connection.cursor()
    cursor.execute(
        """INSERT INTO avg_data (date_time, moisture_reading) 
        VALUES (?, ?)
        ON CONFLICT(date_time)
        DO UPDATE SET moisture_reading = excluded.moisture_reading""",
        (one_hour_ago, average_reading),
    )
    print(f"Wrote to DB -- TIME:{one_hour_ago}, READING:{average_reading}")
    connection.commit()
    connection.close()


average_raw_data()
