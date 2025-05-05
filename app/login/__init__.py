# This defines the blueprint, like creating a room layout
from flask import Blueprint
login_bp = Blueprint("login", __name__, template_folder="templates")
from . import login

