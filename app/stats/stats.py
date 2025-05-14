from flask import render_template
from . import stats_bp
import db


@stats_bp.route("/stats")
def show_stats():
    min_moisture = db.fetch(
        "avg_data", 1, column="moisture_reading", select="MIN(moisture_reading)"
    )

    max_moisture = db.fetch(
        "avg_data", 1, column="moisture_reading", select="MAX(moisture_reading)"
    )

    avg_moisture = int(
        round(
            db.fetch(
                "avg_data", 1, column="moisture_reading", select="AVG(moisture_reading)"
            ),
            0,
        )
    )

    # wifi_strength =

    return render_template(
        "stats.html",
        min_moisture=min_moisture,
        max_moisture=max_moisture,
        avg_moisture=avg_moisture,
    )
