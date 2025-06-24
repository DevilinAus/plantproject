from flask import render_template
from app.charts.get_chart_data import get_chart_data

from . import charts_bp


@charts_bp.route("/charts")
def show_charts():
    data = get_chart_data("1m")

    return render_template("charts.html", data=data)
