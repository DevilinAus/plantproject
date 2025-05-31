import datetime
import requests
import json
from apscheduler.schedulers.blocking import BlockingScheduler
from app.db.models import RawData
from config import ARDUINO_IP

from sqlalchemy import create_engine
from sqlalchemy.orm import Session

# Create standalone version of the engine, so it's not reliant on Flask running.
engine = create_engine("sqlite:///instance/plant_info.db", future=True)


# Copy of the storing function, again so not reliant on the Flask app.
def store_data_arduino(model_class, timestamp: int, value: int):
    with Session(engine) as session:
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
    time_collected = int(datetime.datetime.now().timestamp())
    last_generated = int(get_sensor_data())

    store_data_arduino(RawData, time_collected, last_generated)


scheduler = BlockingScheduler()
scheduler.add_job(main, "interval", minutes=1)
scheduler.start()
