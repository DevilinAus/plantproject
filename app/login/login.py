from flask import render_template, request, flash
from flask_login import login_user, login_required, logout_user, current_user
import sqlite3
import flask_login
import flask
from . import login_bp


# # login_manager = flask_login.LoginManager()
# login_manager.init_app(app)

# mock database for now
# users = {'andrew': {'password': '12345'}}

# class User(flask_login.UserMixin):
#     pass

# @login_manager.user_loader
# def user_loader(email):
#     if email not in users:
#         return

#     user = User()
#     user.id = email
#     return user


# @login_manager.request_loader
# def request_loader(request):
#     email = request.form.get('email')
#     if email not in users:
#         return

#     user = User()
#     user.id = email
#     return user

@login_bp.route("/login", methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        
        # # username = request.form.get('username')

        # if email in users and flask.request.form['password'] == users[email]['password']:
        #     # user = User()
        #     user.id = email
        #     flask_login.login_user(user)
        #     return flask.redirect(flask.url_for('protected'))

        # return 'Bad login'
        # if len(username) == 1:
        #     flash('Username must not be empty.', category='error')

        
        # if username == user:
        #     flash('Logged in successfully!', category='success')
        # else:
        #     flash('Failed to log in.', category='error')

    # data = request.form
    # print(data)

    return render_template("login.html")

