from flask import Flask

from blueprints import homepage
from blueprints.charts import api, charts
from blueprints.auth.login import login

import secrets

app = Flask(__name__)
app.secret_key = secrets.token_hex(32) 
#TODO - figure out how to make this not refresh on every launch


app.register_blueprint(homepage.homepage_bp)
app.register_blueprint(charts.charts_bp)
app.register_blueprint(api.api_bp)
app.register_blueprint(login.login_bp)


if __name__ == "__main__":
    app.run(debug=True)
