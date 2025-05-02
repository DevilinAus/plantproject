from flask import Blueprint, render_template, request, flash
import sqlite3


login_bp = Blueprint("login", __name__, template_folder="templates")


@login_bp.route("/login", methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        username = request.form.get('username')

        if len(username) == 1:
            flash('Username must not be empty.', category='error')

    # data = request.form
    # print(data)

    return render_template("login.html")