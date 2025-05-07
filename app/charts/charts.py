from flask import render_template

import sqlite3
import random
import time


from . import charts_bp


@charts_bp.route("/charts")
def show_charts():
    # Reconnect to the DB
    connection = sqlite3.connect("plant_info.db")
    cursor = connection.cursor()

    # Fetch the last 30 entries of moisture data from the database and assign them to a variable
    cursor.execute("SELECT * FROM minute_reading ORDER BY date_time DESC LIMIT 1440")
    # rows = cursor.fetchall()

    # Close the connection
    connection.close()

    return render_template(
        "charts.html", labels=[10, None, None, 40], values=[30, None, None, 60]
    )
