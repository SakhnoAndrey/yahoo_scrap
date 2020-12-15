from flask import Flask
from flask_migrate import Migrate
from scrap_app.extensions import db
from settings import ConfigBase
from scrap_app.models import Company
from blueprints import bp_rest


def create_app() -> Flask:
    app = Flask(__name__)
    config = ConfigBase()
    scrap_app.config.from_object(config)
    db.init_app(scrap_app)
    migrate = Migrate(scrap_app, db)
    scrap_app.register_blueprint(bp_rest)
    return app


scrap_app = create_app()


@scrap_app.shell_context_processor
def make_shell_context():
    return {"db": db, "Company": Company}


if __name__ == "__main__":
    scrap_app.run("127.0.0.1", "5000", debug=False)
