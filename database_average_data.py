import sqlite3
import datetime
from datetime import timedelta
from apscheduler.schedulers.blocking import BlockingScheduler
import db
from db import get_connection
from config import DB_PATH


def round_down_to_hour(timestamp):
    return timestamp - (timestamp % 3600)

def average_raw_data_loop():

# Otherwise you could have new data processed and stored in the DB out of order?
def average_raw_data_loop(full_run=0):
    start_time = datetime.datetime.now()
    start_time = start_time.timestamp()

    # get the earliest point in the database.

    oldest_timestamp = db.fetch("raw_data", 1, order="ASC")
    oldest_timestamp = oldest_timestamp[0][0]
    print(oldest_timestamp)
    print(type(oldest_timestamp))
    oldest_rounded_down = round_down_to_hour(oldest_timestamp)

    while oldest_rounded_down < start_time:
        print("Starting loop from start of found values")
        average_raw_data(oldest_rounded_down)
        oldest_rounded_down += 3600

    # current_timestamp = last_checkpoint
    # print(current_timestamp)
    # while

    # average_raw_data(start_time)

    # get list of unfinalised data.
    # unfinalised_data =

    # loop them into average_raw_data()

    # update last_finalised in data checkpoint DB


def average_raw_data(timestamp_to_process):
    print("Average Raw Data Processing!")

    # work out what timestamp it was an hour ago(start)
    one_hour_ago = timestamp_to_process - 3600

    print(f"Timestamp to process is: {timestamp_to_process}")
    print(f"An hour ago is: {one_hour_ago}")

    # Fetch data
    rows = db.fetch_between("raw_data", timestamp_to_process, one_hour_ago)

    # count how many data points
    reading_count = 0
    total_reading_value = 0

    for row in rows:
        reading_count += 1
        total_reading_value += row[1]

    # Same as the above but untested.
    # reading_count = len(rows)
    # total_reading_value = sum(row[1] for row in rows)

    print(reading_count)
    print(total_reading_value)

    # add data up & divide by count (get average)
    if reading_count > 0:
        average_reading = round(total_reading_value / reading_count)
    else:
        average_reading = None

    write_to_db(one_hour_ago, average_reading, get_connection())


def write_to_db(one_hour_ago, average_reading, connection):
    cursor = connection.cursor()
    cursor.execute(
        """INSERT INTO avg_data (date_time, moisture_reading)
        VALUES (?, ?)
        ON CONFLICT(date_time)
        DO UPDATE SET moisture_reading = excluded.moisture_reading""",
        (one_hour_ago, average_reading),
    )
    print(f"Wrote to DB -- TIMESTAMP: {one_hour_ago}, READING: {average_reading}")
    connection.commit()
    connection.close()


def main():
    average_raw_data_loop()
    scheduler = BlockingScheduler()
    scheduler.add_job(average_raw_data_loop, "interval", hours=1)
    scheduler.start()

main()
