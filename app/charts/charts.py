from flask import render_template
from app.db.database import db

from . import charts_bp

# sample test data
data = [
    {"x": "2025-05-01T10:00:00", "y": 30},
    {"x": "2025-05-01T11:00:00", "y": 35},
    {"x": "2025-05-01T12:00:00", "y": 28},
]


@charts_bp.route("/charts")
def show_charts():
    # with db.session as session:
    #     pass

    return render_template("charts.html", data=data)
