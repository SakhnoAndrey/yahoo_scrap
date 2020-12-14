from flask import Flask
from flask_migrate import Migrate
from scrap_app.extensions import db
from settings import ConfigBase
from scrap_app.models import Company
import json

scrap_app = Flask(__name__)
scrap_app.config.from_object(ConfigBase)
db.init_app(scrap_app)
migrate = Migrate(scrap_app, db)


@scrap_app.route("/company/<name>")
def get_company_data(name):
    # data = Company.query.filter(Company.name == name).first()
    # return json.dumps(data)
    return name
