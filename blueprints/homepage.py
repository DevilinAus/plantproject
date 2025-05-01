from flask import render_template
from flask import Blueprint
import sqlite3

homepage_bp = Blueprint("homepage", __name__, template_folder="templates")


@homepage_bp.route("/")
def index():

    # Reconnect to the DB
    connection = sqlite3.connect("plant_info.db")
    cursor = connection.cursor()

    # Fetch the last 30 entries of moisture data from the database and assign them to a variable
    cursor.execute("SELECT * FROM minute_reading ORDER BY date_time DESC LIMIT 1")
    rows = cursor.fetchone()
    raw_moisture_reading = rows[1]

    # Close the connection
    connection.close()

    current_moisture = translate_moisture(raw_moisture_reading)

    # print(current_moisture)

    # fake = [{"percent" : 23, "box_colour" : "green"}]

    # Give data to the html
    # return render_template('index.html', monthly_moisture=monthly_moisture)
    # return render_template('index.html', monthly_moisture=map(to_model,rows))
    # print(list(map(to_model,rows)))
    return render_template("index.html", current_moisture=current_moisture)


def translate_moisture(reading):

    # assume zero to be currently wet.
    # 500 seems to maximum reading in air, unsure about soil

    if reading == 0:
        translated_moisture_string = f"Can't get any wetter! <br/> Reading: {reading} <br/> Wetness Estimation: {(500-reading)/5}%"
    elif reading <= 100:
        translated_moisture_string = (
            f"Soaked! <br/> Reading: {reading} <br/> Wetness Estimation: {(500-reading)/5}%"
        )
    elif reading <= 200:
        translated_moisture_string = (
            f"Nice and moist! <br/> Reading: {reading} <br/> Wetness Estimation: {(500-reading)/5}%"
        )
    elif reading <= 300:
        translated_moisture_string = f"Average, if no rain due consider watering! <br/> Reading: {reading} <br/> Wetness Estimation: {(500-reading)/5}%"
    elif reading <= 400:
        translated_moisture_string = f"It's time to water! <br/> Reading: {reading} <br/> Wetness Estimation: {(500-reading)/5}%"
    elif reading <= 400:
        translated_moisture_string = f"Sahara Desert, they're probably dead. Water immediately! <br/> Reading: {reading} <br/> Wetness Estimation: {(500-reading)/5}%"

    return translated_moisture_string
