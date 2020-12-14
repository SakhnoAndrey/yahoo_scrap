from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from models import Company
import json

scrap_app = Flask(__name__)

db = SQLAlchemy(scrap_app)
migrate = Migrate(scrap_app, db)


@app.route("/company/{name}")
def get_data(name):
    data = Company.query.filter(Company.name == name).first()
    return json.dumps(data)
