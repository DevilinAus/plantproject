from flask import Blueprint, request
from .prepare_data import prepare_data

get_chart_data_bp = Blueprint(
    "get_chart_data", __name__, url_prefix="/api", template_folder="templates"
)


@get_chart_data_bp.route("/get_chart_data", methods=["POST"])
def get_chart_data():
    
    data = request.get_json()

    timeframe = data.get("timeframe")
    print("Received timeframe:", timeframe)

    print("sending data to client")
    return prepare_data(timeframe)
