from flask import Flask
from flask_migrate import Migrate
from extensions import db
from settings import ConfigBase
from models import Company
import json

scrap_app = Flask(__name__)
scrap_app.config.from_object(ConfigBase)
migrate = Migrate(scrap_app, db)


@scrap_app.route("/company/<name>")
def get_data(name):
    data = Company.query.filter(Company.name == name).first()
    return json.dumps(data)
