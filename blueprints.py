from flask import Blueprint
from scrap_app import services

bp_rest = Blueprint("bp_rest", __name__)


@bp_rest.route("/company/<name>")
def get_company_data(name):
    # if config.SCRAPPER_TYPE_NAME.lower() == "docker":
    #     scraper = DockerScraper(config)
    # else:
    #     scraper = BrowserScraper(config)
    # json_data = scraper.fetch_data_for(company_name=name)
    # save_company_data(name=name, data=json_data)
    return services.get_company_data(name=name)
