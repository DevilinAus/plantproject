import sqlite3
from datetime import datetime, timedelta
from config import MAX_DATA_POINTS
import db


def get_max_data_points(timeframe):
    data_limit = MAX_DATA_POINTS.get(timeframe, 0)
    return data_limit


def prepare_data(timeframe):
    # lookup the timeframe against max_data_point dict, if it isn't found returns default 0
    data_points = get_max_data_points(timeframe)

    rows = db.fetch("avg_data", data_points)

    response_data = {
        "labels": [None] * data_points,
        "values": [None] * data_points,
    }

    now = datetime.now()
    rounded_now = now.replace(minute=0, second=0, microsecond=0)

    # SET LABELS
    if timeframe == "1d":
        for i in range(data_points):  # 0-24
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

    print(f"returning data \n: {response_data}")
    return response_data
