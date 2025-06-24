from flask import Blueprint, request
from .get_chart_data import get_chart_data, prepare_dashboard_info

api_bp = Blueprint("api", __name__, url_prefix="/api", template_folder="templates")


@api_bp.route("/readings", methods=["GET"])
def get_readings():
    timeframe = request.args.get("timeframe")

    return get_chart_data(timeframe)


@api_bp.route("/dashboard", methods=["GET"])
def get_dashboard_info():
    dashboard_info = prepare_dashboard_info()

    print("sending data to dashboard")
    return dashboard_info
