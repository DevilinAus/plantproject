from dataclasses import asdict
from flask import Flask, jsonify, redirect, render_template, request, url_for
from app.db.database import db


from flask_login import (
    LoginManager,
    login_user,
    login_required,
    logout_user,
    current_user,
)

from app.db.models import Person


from . import admin_bp


@admin_bp.route("/")
@login_required
def index():
    return render_template("admin.html")


@admin_bp.route("/users/create", methods=["GET", "POST"])
def user_create():
    if request.method == "GET":
        user = Person(
            username="andrew",
            email="andrew.daniels@live.com",
            # username=request.form["username"],
            # email=request.form["email"],
        )
        db.session.add(user)
        db.session.commit()
        return redirect(url_for("user_detail", id=user.id))

    return "test"
    # return render_template("user/create.html")


# list user
@admin_bp.route("/users")
def user_list():
    users = db.session.execute(db.select(Person).order_by(Person.username)).scalars()
    print(f"users = {users}")
    users_list = [asdict(user) for user in users]
    return jsonify(users_list)
    # return render_template("user/list.html", users=users)


# view user
@admin_bp.route("/user/<int:id>")
def user_detail(id):
    user = db.get_or_404(Person, id)
    # user = db.get_or_404(Person, id)

    return jsonify(user)
    # return render_template("user/detail.html", user=user)
