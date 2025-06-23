import datetime
import requests
import json
from apscheduler.schedulers.blocking import BlockingScheduler
from scripts.db.vanilla_db import get_engine_and_session
from models.models import RawData
from config import ARDUINO_IP


def store_data_arduino(model_class, timestamp: int, value: int, SessionLocal):
    with SessionLocal() as session:
        new_entry = model_class(timestamp=timestamp, value=value)

        session.add(new_entry)
        session.commit()


def get_sensor_data():
    url = f"http://{ARDUINO_IP}/sensor"

    response = requests.get(url)

    try:
        if response.status_code == 200:
            sensor_data = json.loads(response.text)
            sensor_data = int(sensor_data["sensor"])

            print(f"Sensor Data: {sensor_data}")
            return sensor_data
        else:
            print(f"Failed to get data. Status code: {response.status_code}")
            return None

    except requests.exceptions.RequestException as e:
        print(f"{e}")
        return None


def main():
    _, SessionLocal = get_engine_and_session()
    time_collected = int(datetime.datetime.now().timestamp())
    last_generated = int(get_sensor_data())

    store_data_arduino(RawData, time_collected, last_generated, SessionLocal)


scheduler = BlockingScheduler()
scheduler.add_job(main, "interval", minutes=1)
scheduler.start()
