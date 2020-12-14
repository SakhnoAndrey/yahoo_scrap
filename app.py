from flask import Flask
from flask_migrate import Migrate
from scrap_app.extensions import db
from settings import ConfigBase
from scrapping import DockerScraper, BrowserScraper
from scrap_app.models import Company
from scrap_app.services import save_company_data

scrap_app = Flask(__name__)
config = ConfigBase()
scrap_app.config.from_object(config)
db.init_app(scrap_app)
migrate = Migrate(scrap_app, db)


@scrap_app.route("/company/<name>")
def get_company_data(name):
    if config.SCRAPPER_TYPE_NAME.lower() == "docker":
        scraper = DockerScraper(config)
    else:
        scraper = BrowserScraper(config)
    json_data = scraper.fetch_data_for(company_name=name)
    save_company_data(name=name, data=json_data)


@scrap_app.shell_context_processor
def make_shell_context():
    return {"db": db, "Company": Company}


if __name__ == "__main__":
    scrap_app.run("127.0.0.1", "5000", debug=False)
