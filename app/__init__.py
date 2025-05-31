# This builds the Flask app and returns it

from flask import Flask
import os
from app.db.database import db


from flask_login import LoginManager
import secrets

from app.user import User, users

login_manager = LoginManager()


@login_manager.user_loader
def user_loader(email):
    if email not in users:
        return

    user = User()
    user.id = email
    return user


@login_manager.request_loader
def request_loader(request):
    email = request.form.get("email")
    if email not in users:
        return

    user = User()
    user.id = email
    return user


def create_app():
    app = Flask(__name__)

    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///plant_info.db"
    # used user management. (sessions / messages etc.) now being created after the app is initalised.
    app.secret_key = secrets.token_hex(32)
    # TODO - figure out how to make this not refresh on every launch

    login_manager.init_app(app)
    login_manager.login_view = "auth.login"

    db.init_app(app)

    # Import blueprints here AFTER app is created

    from app.index import index_bp
    from app.charts import charts_bp
    from app.auth import auth_bp
    from app.admin import admin_bp
    from app.charts.api import api_bp
    from app.stats import stats_bp
    from app.dashboard import dashboard_bp
    from app.integrations.weather_api import weather_api_bp

    app.register_blueprint(index_bp)
    app.register_blueprint(charts_bp)
    app.register_blueprint(auth_bp)
    app.register_blueprint(admin_bp)
    app.register_blueprint(api_bp)
    app.register_blueprint(stats_bp)
    app.register_blueprint(dashboard_bp)
    app.register_blueprint(weather_api_bp)

    with app.app_context():
        db.create_all()

    return app
