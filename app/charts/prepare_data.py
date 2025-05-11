import sqlite3
from datetime import datetime, timedelta

max_data_points = {"1d": 24, "1w": 10080, "1m": 44640}


def prepare_data(timeframe):
    # lookup the timeframe against max_data_point dict, if it isn't found returns default 0
    data_limit = max_data_points.get(timeframe, 0)

    # Reconnect to the DB
    connection = sqlite3.connect("plant_info.db")
    cursor = connection.cursor()

    if timeframe == "1d":
        cursor.execute(
            "SELECT * FROM avg_data ORDER BY date_time DESC LIMIT ?", (data_limit,)
        )
        rows = cursor.fetchall()

    # Close the connection
    connection.close()

    response_data = {
        "labels": [None] * max_data_points[timeframe],
        "values": [None] * max_data_points[timeframe],
    }

    now = datetime.now()
    rounded_now = now.replace(minute=0, second=0, microsecond=0)

    # SET LABELS
    if timeframe == "1d":
        for i in range(max_data_points[timeframe]):  # 0-24
            unformatted_time = rounded_now - timedelta(hours=i)
            formatted_time = unformatted_time.strftime("%I:%M %p")
            response_data["labels"][i] = formatted_time

    print(f"Response_data = {response_data}")

    for i, row in enumerate(rows):
        current_value = row[1]
        datetime_str = row[0]
        datetime_obj = datetime.strptime(datetime_str, "%Y-%m-%d %H:%M:%S")
        formatted_time_2 = datetime_obj.strftime("%I:%M %p")

        for j, label in enumerate(response_data["labels"]):
            print(
                f"Formatted Time2= {formatted_time_2}. Response_data label= {response_data['labels'][j]}"
            )
            if formatted_time_2 == response_data["labels"][j]:
                # response_data["values"] = row[1]
                print(f"TRUE || {formatted_time_2} = {response_data['labels'][j]}")
                response_data["values"][j] = current_value
        # internal loop, loop the row label through all the options in the response data

        # print(f"setting value")
        # print(datetime_obj)
        # formatted_row = raw_row.strftime("%I:%M %p")

    #     for j in response_data["labels"]:
    #         if response_data["labels"][j] == rows[i]:
    #             response_data["values"][j] = rows[i]

    print(f"returning data \n: {response_data}")
    return response_data
