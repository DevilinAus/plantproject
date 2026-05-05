from flask import render_template
from sqlalchemy import func, select
from models.models import AvgData, RawData
from . import index_bp
from app.db.flask_db import db


@index_bp.route("/")
def show_homepage():
    latest_raw_query = select(RawData.value).order_by(RawData.id.desc()).limit(1)
    maximum_raw_query = select(func.max(RawData.value))
    latest_avg_query = select(AvgData.value).order_by(AvgData.id.desc()).limit(1)
    maximum_avg_query = select(func.max(AvgData.value))

    latest_raw_reading = db.session.execute(latest_raw_query).scalar_one_or_none()
    maximum_raw_value = db.session.execute(maximum_raw_query).scalar_one_or_none()
    latest_avg_reading = db.session.execute(latest_avg_query).scalar_one_or_none()
    maximum_avg_value = db.session.execute(maximum_avg_query).scalar_one_or_none()

    current_reading = first_numeric(latest_raw_reading, latest_avg_reading, 138)
    max_value = first_numeric(maximum_raw_value, maximum_avg_value, 190)

    current_moisture = translate_moisture(current_reading, max_value)

    return render_template("index.html", current_moisture=current_moisture)


def first_numeric(*values):
    for value in values:
        parsed_value = parse_numeric(value)
        if parsed_value is not None:
            return parsed_value

    return None


def parse_numeric(value):
    if isinstance(value, bool):
        return None

    if isinstance(value, (int, float)):
        return float(value)

    if isinstance(value, str):
        try:
            return float(value)
        except ValueError:
            return None

    return None


def translate_moisture(reading, max_wet):
    if reading is None or max_wet is None or int(max_wet) <= 0:
        return (
            "Moisture data syncing. <br/> Demo values are loading for the dashboard."
        )

    percent_value = int((reading / max_wet) * 100)
    reading = int(round(reading))

    # Added subnautica themed warnings, I might want to update these to be an option when app is more complete.
    # Maybe a few different "themes" for the warnings, that could tie in with the tailwind theme"
    if reading < 50:
        return f"Moisture levels critical. <br/> Oversaturation detected - Root suffocation likely. <br/> Reading: {reading} <br/> Wetness Estimation: {percent_value}%"
    elif reading <= 100:
        return f"Moisture levels balanced. <br/> Additional H₂O not recommended. <br/> Reading: {reading} <br/> Wetness Estimation: {percent_value}%"
    elif reading <= 150:
        return f"Moisture within acceptable parameters. </br> No action required. <br/> Reading: {reading} <br/> Wetness Estimation: {percent_value}%"
    elif reading <= 200:
        return f"Moisture decreasing. <br/> Recommend hydration soon to avoid cellular stress. <br/> Reading: {reading} <br/> Wetness Estimation: {percent_value}%"
    elif reading <= 250:
        return f"Warning: Dry conditions detected. </br> Hydration required to prevent plant stress. <br/> Reading: {reading} <br/> Wetness Estimation: {percent_value}%"
    elif reading <= 300:
        return f"Alert: Severe dehydration likely.  </br> Survival chances declining. <br/> Reading: {reading} <br/> Wetness Estimation: {percent_value}%"
    elif reading > 300 and reading < 500:
        return f"CRITICAL STATUS! <br/> Substrate moisture insufficient to support biological activity. </br> Initiate emergency hydration protocol. <br/> Reading: {reading} <br/> Wetness Estimation: {percent_value}%"
    else:
        return "Reading outside expected parameters. Consult administrator."
