from flask import Flask
import sqlite3

from blueprints.charts import charts
from blueprints import homepage

app = Flask(__name__)

# app.register_blueprint(homepage.homepage_bp)
# app.register_blueprint(rolling_days.rolling_days_bp)
# app.register_blueprint(daily.daily_bp)
app.register_blueprint(charts.charts_bp)
app.register_blueprint(homepage.homepage_bp)
# app.register_blueprint(daily_chart.daily_chart_bp)
#app.register_blueprint(calendar_bp, url_prefix='/calendar')

#Set this to 1 if you need to recreate the table.
# create_moist_db = 0

# if create_moist_db == 1:
#     connection = sqlite3.connect("plant_info.db")
#     cursor = connection.cursor()
#     cursor.execute("create table moist (date_time text, wetness integer, box_colour text)")
#     cursor.execute("create table hourly (date_time text, wetness integer)")

if __name__ == "__main__":
    app.run(debug=True)

