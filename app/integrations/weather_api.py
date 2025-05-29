from dotenv import load_dotenv
import requests
import os
import db
from flask import Blueprint
import time

weather_api_bp = Blueprint(
    "weather_api", __name__, url_prefix="/integrations", template_folder="templates"
)

load_dotenv()
API_KEY = os.getenv("WEATHER_API_KEY")
CITY = "Brisbane"

# Current weather.
current_query = (
    f"https://api.weatherapi.com/v1/current.json?key={API_KEY}&q={CITY}&aqi=no"
)

forecast_query = f"https://api.weatherapi.com/v1/forecast.json?key={API_KEY}&q={CITY}&days=3&aqi=no&alerts=no"


@weather_api_bp.route("/get_weather", methods=["GET"])
def get_weather():
    now = int(time.time())
    collected_at = db.fetch_collected_at()

    if (now - int(collected_at)) > 300:
        fetch_external_data(now)

    db_data = db.fetch_all("current_weather")

    print(db_data)

    return db_data


def fetch_external_data(now):
    response = requests.get(current_query)
    current_weather = response.json()

    if response.status_code == 200:
        pass
    else:
        print(f"Failed to fetch data: {current_weather.status_code}")

    for key, value in current_weather["current"].items():
        if key != "condition":
            db.store_weather(key, value)

    for key, value in current_weather["current"]["condition"].items():
        db.store_weather(key, value)

    db.store_weather("fetched_at", now)
