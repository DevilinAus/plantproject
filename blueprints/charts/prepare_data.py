import sqlite3

max_data_points = {
    "1d": 1440, 
    "1w": 10080, 
    "1m": 44640
    }


def prepare_data(timeframe):

    # lookup the timeframe against max_data_point dict, if it isn't found returns default 0
    data_limit = max_data_points.get(timeframe, 0)

    # Reconnect to the DB
    connection = sqlite3.connect("plant_info.db")
    cursor = connection.cursor()

    # Fetch the last 30 entries of moisture data from the database and assign them to a variable
    cursor.execute("SELECT * FROM minute_reading ORDER BY date_time DESC LIMIT ?", (data_limit,))
    rows = cursor.fetchall()

    # Close the connection
    connection.close()

    # sample_data = {
    #     "labels": ["2025-05-01 10:00", "2025-05-01 11:00", "2025-05-01 12:00"],
    #     "values": [30, 35, 28],
    # }

    response_data = {
        "labels": [], 
        "values": [],
    }

    # TODO - Need to keep values for the last day only (if the device has been turned off the )
    #last 1440 could include old data.

    # TODO - NEED TO DO SOME AVERAGING MATH ON THIS DATA BEFORE ADDING IT TO DICT SO IT HAS ONE VALUE
    # PER HOUR NOT 60 PER HOUR AND GENERATE NEW LABELS. (maybe less for weekly/monthly? )
    for row in rows:
        response_data["labels"].append(row[0])
        response_data["values"].append(row[1])

    # print(map(to_model, rows))

    print("returning data")
    return response_data


# def to_model(row):

#     model = {
#         "date_time": row[0],
#         "percent": row[1],
#     }

#     return model
