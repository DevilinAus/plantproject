from flask import Blueprint
index_bp = Blueprint("index", __name__, template_folder="templates")
from . import home  # noqa: E402, F401


