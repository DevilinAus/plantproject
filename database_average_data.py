import sqlite3
import datetime
from datetime import timedelta
from apscheduler.schedulers.blocking import BlockingScheduler
import db


def average_raw_data_loop(full_run=0):
    start_time = datetime.datetime.now()
    start_time = start_time.timestamp()

    #get the last finalised time 
    last_finalised = db.fetch("data_checkpoint",1)

    # get list of unfinalised data.
    unfinalised_data =  

    #loop them into average_raw_data()

    #update last_finalised in data checkpoint DB

# TODO make this function scaleable - it would be good if it could be passed in the hour so it
# could loop over hours gone.
def average_raw_data():
    print("Average Raw Data Processing!")
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

    # Fetch data
    rows = db.fetch_between(one_hour_ago_timestamp, now_timestamp)
    
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

    print(average_reading)

    db.store_data(now_timestamp,  )

                # store that data with current date and hour (for label) in cleaned DB.
                connection = sqlite3.connect("plant_info.db")
                cursor = connection.cursor()
                cursor.execute(
                    """INSERT INTO avg_data (date_time, readable_text, moisture_reading) 
                    VALUES (?, ?, ?)
                    ON CONFLICT(date_time)
                    DO UPDATE SET moisture_reading = excluded.moisture_reading""",
                    (one_hour_ago_timestamp, one_hour_ago, average_reading),
                )
                print(
                    f"Wrote to DB -- TIMESTAMP: {one_hour_ago_timestamp} READBLE: {one_hour_ago}, READING: {average_reading}"
                )
                connection.commit()
                connection.close()


scheduler = BlockingScheduler()
scheduler.add_job(average_raw_data, "interval", hours=1)
scheduler.start()

# average_raw_data()
