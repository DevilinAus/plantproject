import time
from sqlalchemy import select
from models.models import AvgData, RawData
from app.db.flask_db import db

HOURS_DICT = {"1d": 24, "1w": 168, "1m": 720}  # currently assuming 1month = 30days.


def get_max_data_points(timeframe):
    hours_to_fetch = HOURS_DICT.get(timeframe, 0)
    return hours_to_fetch


def round_down_to_hour(timestamp):
    return timestamp - (timestamp % 3600)


def construct_datapoint(label, value):
    label = label * 1000
    return {"x": label, "y": value}


def get_chart_data(timeframe):
    hours_to_fetch = get_max_data_points(timeframe)

    now = int(time.time())
    end_time = round_down_to_hour(now)
    start_time = end_time - (hours_to_fetch * 3600)

    query = select(AvgData).where(
        (AvgData.timestamp >= start_time) & (AvgData.timestamp <= end_time)
    )

    rows = db.session.execute(query).scalars().all()

    response_data = []

    for row in rows:
        label = row.timestamp
        value = row.value

        current_datapoint = construct_datapoint(label, value)
        response_data.append(current_datapoint)

    return response_data


def prepare_dashboard_info():
    latest_query = select(RawData.value).order_by(RawData.id.desc()).limit(1)

    latest_raw_reading = db.session.execute(latest_query).scalar_one_or_none()

    return {"status": "Healthy", "moisture": latest_raw_reading}
