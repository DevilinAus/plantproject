from flask import Flask

# from app.index import index
# from app.charts import api, charts
# from app.auth.login import login
from app import create_app

app = create_app()
if __name__ == "__main__":
    app.run(debug=True)
