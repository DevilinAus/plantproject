from flask import Blueprint

charts_bp = Blueprint("charts", __name__, template_folder="templates")
from . import charts  # noqa: E402, F401