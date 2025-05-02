from flask import Blueprint, request
from .prepare_data import prepare_data

api_bp = Blueprint(
    "api", __name__, url_prefix="/api", template_folder="templates"
)


@api_bp.route("/readings", methods=["GET"])
def get_readings():
    timeframe = request.args.get('timeframe')
    # data = request.get_json()

    # timeframe = data.get("timeframe")
    print("Received timeframe:", timeframe)

    print("sending data to client")
    return prepare_data(timeframe)
