import os
import time
import requests

from dotenv import load_dotenv
from flask import Blueprint, jsonify
from sqlalchemy import select
from sqlalchemy.dialects.sqlite import insert

from app.db.flask_db import db
from models.models import Weather


weather_api_bp = Blueprint(
    "weather_api", __name__, url_prefix="/integrations", template_folder="templates"
)

load_dotenv()
API_KEY = os.getenv("WEATHER_API_KEY")
CITY = "Brisbane"
FIFTEEN_MINS = 900

# Copy paste these into functions as you need them. Can delete once they've been used.
# current_query = (
#     f"https://api.weatherapi.com/v1/current.json?key={API_KEY}&q={CITY}&aqi=no"
# )
# forecast_query = f"https://api.weatherapi.com/v1/forecast.json?key={API_KEY}&q={CITY}&days=3&aqi=no&alerts=no"


@weather_api_bp.route("/get_weather", methods=["GET"])
def get_weather():
    now = int(time.time())

    last_updated_stmt = select(Weather.id).where(Weather.key == "last_updated_epoch")
    last_updated = db.session.execute(last_updated_stmt).scalar_one_or_none()

    if (last_updated is None) or (now > last_updated + FIFTEEN_MINS):
        fetch_external_data()

    fetch_all_query = select(Weather)
    db_data = db.session.execute(fetch_all_query).scalars().all()

    return jsonify({row.key: row.value for row in db_data})


def fetch_external_data():
    forecast_query = f"https://api.weatherapi.com/v1/forecast.json?key={API_KEY}&q={CITY}&days=3&aqi=no&alerts=no"

    response = requests.get(forecast_query)
    forecast_weather = response.json()

    if response.status_code != 200:
        print(f"Failed to fetch data: {forecast_weather.status_code}")

    # Two loops, there's a nested dict in the external return, unique keys, so this flattens the return.
    for key, value in forecast_weather["current"].items():
        if key != "condition":
            stmt = insert(Weather).values(key=key, value=value)
            stmt = stmt.on_conflict_do_update(
                index_elements=["key"], set_={"value": value}
            )
            db.session.execute(stmt)

    for key, value in forecast_weather["current"]["condition"].items():
        stmt = insert(Weather).values(key=key, value=value)
        stmt = stmt.on_conflict_do_update(index_elements=["key"], set_={"value": value})
        db.session.execute(stmt)

    db.session.commit()
