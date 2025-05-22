from flask import render_template
from . import index_bp
import db


@index_bp.route("/")
def show_homepage():
    # Reconnect to the DB
    connection = db.get_connection()
    cursor = connection.cursor()

    # Fetch the last 30 entries of moisture data from the database and assign them to a variable
    cursor.execute("SELECT * FROM raw_data ORDER BY date_time DESC LIMIT 1")
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
    maximum_value = db.fetch("avg_data", data_limit=1, select="MAX(moisture_reading)")

    if isinstance(reading, (int, float)) and isinstance(maximum_value, (int, float)):
        percent_value = int((reading / maximum_value) * 100)
    else:
        return "Non numberic values provided. Consult administrator"

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
