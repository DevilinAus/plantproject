import sqlite3
import datetime
import requests
import json
from apscheduler.schedulers.blocking import BlockingScheduler
from config import ARDUINO_IP
import time


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
    print("Starting data collection...")

    time_collected = int(datetime.datetime.now().timestamp())
    last_generated = get_sensor_data()

    # TODO - Use External DB Function Here.
    connection = sqlite3.connect("plant_info.db")
    connection.execute("PRAGMA journal_mode=WAL;")
    cursor = connection.cursor()
    cursor.execute(
        "INSERT INTO raw_data (date_time, moisture_reading) VALUES (?, ?)",
        (time_collected, last_generated),
    )
    print(f"Wrote to DB! \nTIME: {time_collected}\nREADING:{last_generated}\n")
    connection.commit()
    connection.close()


scheduler = BlockingScheduler()
scheduler.add_job(main, "interval", minutes=1)
scheduler.start()
