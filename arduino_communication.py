import time
import sqlite3
import datetime
import requests
# from config import ip, finish this when it's not running.

# Define the Ardiuno IP here: NOTE - This is set statically via a static lease on router.
ARDUINO_IP = "192.168.0.99"


def get_sensor_data():
    # Define the url. Can add query parameters here for cool future features
    url = f"http://{ARDUINO_IP}/"

    # Try and connect to the webserver, if response is 200 (good) then get the data.
    try:
        response = requests.get(url)
        if response.status_code == 200:
            # Read the raw sensor data from the response
            sensor_data = int(response.text)  # Convert the response to an integer
            print(f"Sensor Data: {sensor_data}")
            return sensor_data
        else:
            print(f"Failed to get data. Status code: {response.status_code}")
            return 9999
    except requests.exceptions.RequestException as e:
        print(f"Error: {e}")
        return 9999


def wait_calculation():
    # Calculate the time since Epoch
    epoch_time = int(time.time())

    # Calulate how many seconds until the next minute
    seconds_past_min = epoch_time % 60
    seconds_remaining_in_min = 60 - seconds_past_min

    # Sleep until the next min
    time.sleep(seconds_remaining_in_min)


def main():
    print("Application Starting!")
    while True:
        # Run function to figure out how long to sleep until the next minute.
        wait_calculation()

        # Get the reading from the arduino
        time_collected = int(datetime.datetime.now().timestamp())
        print(f" Time Collected: {time_collected}")
        last_generated = get_sensor_data()

        connection = sqlite3.connect("plant_info.db")
        connection.execute("PRAGMA journal_mode=WAL;")
        cursor = connection.cursor()
        cursor.execute(
            "INSERT INTO raw_data (date_time, moisture_reading) VALUES (?, ?)",
            (time_collected, last_generated),
        )
        print(f"Wrote to DB -- TIME:{time_collected}, READING:{last_generated}")
        connection.commit()
        connection.close()


main()
