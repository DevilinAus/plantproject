import db
from db import get_connection, fetch
import time

HOURS_DICT = {"1d": 24, "1w": 168, "1m": 720}  # currently assuming 1month = 30days.


def get_max_data_points(timeframe):
    hours_to_fetch = HOURS_DICT.get(timeframe, 0)
    return hours_to_fetch


def round_down_to_hour(timestamp):
    return timestamp - (timestamp % 3600)


def construct_datapoint(label, value):
    label = label * 1000
    return {"x": label, "y": value}


def prepare_data(timeframe):
    hours_to_fetch = get_max_data_points(timeframe)

    now = int(time.time())
    start_time = round_down_to_hour(now)
    end_time = start_time - (hours_to_fetch * 3600)

    rows = db.fetch_between("avg_data", start_time, end_time)

    response_data = []

    for row in rows:
        label = row[0]
        value = row[1]
        print(f"{label} & {value}")
        current_datapoint = construct_datapoint(label, value)
        response_data.append(current_datapoint)

    return response_data


def prepare_dashboard_info():
    connection = get_connection()

    latest_moisture = fetch(
        "raw:_data", 1, column="date_time", order="DESC", select="moisture_reading"
    )

    connection.close()

    return {"status": "Healthy", "moisture": latest_moisture}
