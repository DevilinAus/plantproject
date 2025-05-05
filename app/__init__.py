# This builds the Flask app and returns it

from flask import Flask

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
    email = request.form.get('email')
    if email not in users:
        return

    user = User()
    user.id = email
    return user

def create_app():
    app = Flask(__name__, )
    # used user management. (sessions / messages etc.) now being created after the app is initalised.
    app.secret_key = secrets.token_hex(32) 
    #TODO - figure out how to make this not refresh on every launch
    
    
    login_manager.init_app(app)


    


    # Import blueprints here AFTER app is created
    
    from app.index import index_bp
    from app.charts import charts_bp
    from app.login import login_bp


   
    app.register_blueprint(index_bp)
    app.register_blueprint(charts_bp)
    app.register_blueprint(login_bp)

    return app

