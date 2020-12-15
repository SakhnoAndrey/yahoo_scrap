from flask import Flask
from flask_migrate import Migrate
from scrap_app.extensions import db
from settings import ConfigBase
from blueprints import bp_rest


def create_app() -> Flask:
    application = Flask(__name__)
    config = ConfigBase()
    application.config.from_object(config)
    db.init_app(application)
    migrate = Migrate(application, db)
    application.register_blueprint(bp_rest)
    return application
