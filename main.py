from flask import Flask


from blueprints import homepage
from blueprints.charts import charts, get_chart_data

app = Flask(__name__)


app.register_blueprint(homepage.homepage_bp)
app.register_blueprint(charts.charts_bp)
app.register_blueprint(get_chart_data.get_chart_data_bp)


if __name__ == "__main__":
    app.run(debug=True)
