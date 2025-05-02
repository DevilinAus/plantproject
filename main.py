from flask import Flask


from blueprints import homepage
from blueprints.charts import api, charts
from blueprints.auth.login import login

app = Flask(__name__)


app.register_blueprint(homepage.homepage_bp)
app.register_blueprint(charts.charts_bp)
app.register_blueprint(api.api_bp)
app.register_blueprint(login.login_bp)


if __name__ == "__main__":
    app.run(debug=True)
