from flask import render_template
from . import stats_bp
import db


@stats_bp.route("/stats")
def show_stats():
    min_moisture = db.fetch("avg_data", 1, column="value", select="MIN(value)")
    max_moisture = db.fetch("avg_data", 1, column="value", select="MAX(value)")
    avg_moisture = db.fetch("avg_data", 1, column="value", select="AVG(value)")

    if avg_moisture is not None:
        avg_moisture = int(round(avg_moisture, 0))

    min_moisture = min_moisture if min_moisture is not None else "No data yet"
    max_moisture = max_moisture if max_moisture is not None else "No data yet"
    avg_moisture = avg_moisture if avg_moisture is not None else "No data yet"

    # Demo placeholders until live Arduino stats are wired into the page.
    wifi_strength = "-58 dBm"
    data_logged_completion = "100%"
    device_status = "Online"

    return render_template(
        "stats.html",
        min_moisture=min_moisture,
        max_moisture=max_moisture,
        avg_moisture=avg_moisture,
        wifi_strength=wifi_strength,
        data_logged_completion=data_logged_completion,
        device_status=device_status,
    )
