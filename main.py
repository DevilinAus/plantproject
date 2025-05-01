from flask import Flask

from blueprints.charts import charts
from blueprints import homepage

app = Flask(__name__)

app.register_blueprint(charts.charts_bp)
app.register_blueprint(homepage.homepage_bp)

if __name__ == "__main__":
    app.run(debug=True)
