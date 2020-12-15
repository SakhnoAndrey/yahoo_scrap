import logging
from rest_app.app import create_app
from scrap_app.browser_scraper import BrowserScraper
from scrap_app.docker_scraper import DockerScraper
from settings import ConfigBase

logging.getLogger().setLevel(logging.INFO)


if __name__ == "__main__":
    config = ConfigBase()
    print(
        "Scraping with {0}.{1}".format(config.SCRAPPER_TYPE_NAME, config.BROWSER_NAME)
    )
    if config.SCRAPPER_TYPE_NAME == "docker":
        scraper = DockerScraper(config)
    else:
        scraper = BrowserScraper(config)
    scrap_app = create_app()
    with scrap_app.app_context():
        scraper.fetch_data_for(company_names=config.COMPANY_NAMES)
    print("Scraping done")
