from flask import render_template
from db import get_connection

from . import charts_bp

# sample test data
data = [
    {"x": "2025-05-01T10:00:00", "y": 30},
    {"x": "2025-05-01T11:00:00", "y": 35},
    {"x": "2025-05-01T12:00:00", "y": 28},
]


@charts_bp.route("/charts")
def show_charts():
    # Reconnect to the DB
    connection = get_connection()
    cursor = connection.cursor()

    # Fetch the last 30 entries of moisture data from the database and assign them to a variable
    cursor.execute("SELECT * FROM raw_data ORDER BY date_time DESC LIMIT 1440")
    # rows = cursor.fetchall()

    # Close the connection
    connection.close()

    return render_template("charts.html", data=data)
