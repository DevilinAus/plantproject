# This defines the blueprint, like creating a room layout
from flask import Blueprint

auth_bp = Blueprint("auth", __name__, template_folder="templates")
from . import auth
