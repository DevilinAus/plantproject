from flask import Flask, render_template

from flask_login import (
    LoginManager,
    login_user,
    login_required,
    logout_user,
    current_user,
)

from . import admin_bp


@admin_bp.route("/")
@login_required
def index():
    return render_template("admin.html")
