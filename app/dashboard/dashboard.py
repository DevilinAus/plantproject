from flask import render_template
from . import dashboard_bp


@dashboard_bp.route("/dashboard/")
def show_dashboard():
    return render_template("dashboard.html")
