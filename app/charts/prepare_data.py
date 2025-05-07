import sqlite3
import datetime
from datetime import timedelta

max_data_points = {"1d": 24, "1w": 10080, "1m": 44640}


def prepare_data(timeframe):
    # lookup the timeframe against max_data_point dict, if it isn't found returns default 0
    data_limit = max_data_points.get(timeframe, 0)

    # Reconnect to the DB
    connection = sqlite3.connect("plant_info.db")
    cursor = connection.cursor()

    # Fetch the last 30 entries of moisture data from the database and assign them to a variable

    # TODO REMOVE THE MINUTE_READING DB AND IF ELSE STATEMENT ONCE MORE DATA AVERAGED OUT
    if timeframe == "1d":
        cursor.execute(
            "SELECT * FROM avg_data ORDER BY date_time DESC LIMIT ?", (data_limit,)
        )
        rows = cursor.fetchall()
    else:
        cursor.execute(
            "SELECT * FROM minute_reading ORDER BY date_time DESC LIMIT ?",
            (data_limit,),
        )
        rows = cursor.fetchall()

    # Close the connection
    connection.close()

    # sample_data = {
    #     "labels": ["2025-05-01 10:00", "2025-05-01 11:00", "2025-05-01 12:00"],
    #     "values": [30, 35, 28],
    # }
    print(type(max_data_points))

    response_data = {
        "labels": [None] * max_data_points[timeframe],
        "values": [None] * max_data_points[timeframe],
    }

    now = datetime.datetime.now()
    rounded_now = now.replace(minute=0, second=0, microsecond=0)
    # TODO REMOVE THIS & MODIFY TO HANDLE DIFFERENT TIMEFRAMES
    # SET LABELS
    if timeframe == "1d":
        for i in range(max_data_points[timeframe]):  # 0-24
            unformatted_time = rounded_now - timedelta(hours=i)
            formatted_time = unformatted_time.strftime("%I:%M %p")
            response_data["labels"][i] = formatted_time

    print(response_data)

    print(f"Test Printing Rows {rows}")
    # TODO - NEED TO DO SOME AVERAGING MATH ON THIS DATA BEFORE ADDING IT TO DICT SO IT HAS ONE VALUE
    # PER HOUR NOT 60 PER HOUR AND GENERATE NEW LABELS. (maybe less for weekly/monthly? )
    for row in rows:
        response_data["labels"].append(row[0])
        response_data["values"].append(row[1])

    # print(map(to_model, rows))

    print("returning data")
    return response_data
