from flask import render_template
from . import index_bp
import db


@index_bp.route("/")
def show_homepage():
    latest_db_reading = db.fetch_latest("raw_data", select="moisture_reading")
    maximum_value = db.fetch("avg_data", data_limit=1, select="MAX(moisture_reading)")

    current_moisture = translate_moisture(latest_db_reading, maximum_value)

    return render_template("index.html", current_moisture=current_moisture)


def translate_moisture(reading, max_wet):
    if isinstance(reading, (int, float)) and isinstance(max_wet, (int, float)):
        percent_value = int((reading / max_wet) * 100)
    else:
        return "Non numberic values provided. Consult administrator"

    # Added subnautica themed warnings, I might want to update these to be an option when app is more complete.
    # Maybe a few different "themes" for the warnings, that could tie in with the tailwind theme"
    if reading < 50:
        return f"Moisture levels critical. <br/> Oversaturation detected - Root suffocation likely. <br/> Reading: {reading} <br/> Wetness Estimation: {100 - percent_value}%"
    elif reading <= 100:
        return f"Moisture levels balanced. <br/> Additional H₂O not recommended. <br/> Reading: {reading} <br/> Wetness Estimation: {100 - percent_value}%"
    elif reading <= 150:
        return f"Moisture within acceptable parameters. </br> No action required. <br/> Reading: {reading} <br/> Wetness Estimation: {100 - percent_value}%"
    elif reading <= 200:
        return f"Moisture decreasing. <br/> Recommend hydration soon to avoid cellular stress. <br/> Reading: {reading} <br/> Wetness Estimation: {100 - percent_value}%"
    elif reading <= 250:
        return f"Warning: Dry conditions detected. </br> Hydration required to prevent plant stress. <br/> Reading: {reading} <br/> Wetness Estimation: {100 - percent_value}%"
    elif reading <= 300:
        return f"Alert: Severe dehydration likely.  </br> Survival chances declining. <br/> Reading: {reading} <br/> Wetness Estimation: {100 - percent_value}%"
    elif reading > 300 and reading < 500:
        return f"CRITICAL STATUS! <br/> Substrate moisture insufficient to support biological activity. </br> Initiate emergency hydration protocol. <br/> Reading: {100 - reading} <br/> Wetness Estimation: {percent_value}%"
    else:
        return "Reading outside expected parameters. Consult administrator."
