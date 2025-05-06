from flask import render_template, request, flash
from flask_login import login_user, login_required, logout_user, current_user
import sqlite3
import flask_login
import flask

from app.user import User, users
from . import auth_bp


@auth_bp.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password")

        # username = request.form.get('username')

        if (
            email in users
            and flask.request.form["password"] == users[email]["password"]
        ):
            user = User()
            user.id = email
            flask_login.login_user(user)
            flash("Good login", "success")
            return flask.redirect(flask.url_for("charts.show_charts"))

        flash("Invalid login", "error")

    return render_template("login.html")


@auth_bp.route("/logout")
def logout():
    # logout user
    flask_login.logout_user()

    flash("Successfully logged out", "success")

    # redirct to homepage
    return flask.redirect(flask.url_for("index.show_homepage"))
