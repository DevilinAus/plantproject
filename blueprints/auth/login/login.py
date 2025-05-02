from flask import render_template
from flask import Blueprint
import sqlite3
import random
import time

login_bp = Blueprint("login", __name__, template_folder="templates")


@login_bp.route("/login")
def charts():
    pass