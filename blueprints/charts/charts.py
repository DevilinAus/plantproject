from flask import render_template
from flask import Blueprint
import sqlite3
import random
import time

charts_bp = Blueprint("charts", __name__, template_folder="templates")


@charts_bp.route("/charts")
def charts():

    # Reconnect to the DB
    connection = sqlite3.connect("plant_info.db")
    cursor = connection.cursor()

    # Fetch the last 30 entries of moisture data from the database and assign them to a variable
    cursor.execute("SELECT * FROM minute_reading ORDER BY date_time DESC LIMIT 1440")
    # rows = cursor.fetchall()

    # Close the connection
    connection.close()

    return render_template("charts.html", labels=[10, 20, 30, 40], values=[30, 45, 50, 60])


# def to_model(row):

#     model = {
#         "date_time": row[0],
#         "percent": row[1],
#     }

#     return model
