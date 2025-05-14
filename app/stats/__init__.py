from flask import Blueprint

stats_bp = Blueprint("stats", __name__, template_folder="templates")
from . import stats  # noqa: E402, F401
