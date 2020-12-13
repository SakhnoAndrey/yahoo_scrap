from dotenv import load_dotenv
from pathlib import Path
import os

env_path = Path(".") / ".env"
load_dotenv(dotenv_path=env_path, verbose=True)


class ConfigBase:
    DOCKER_BOOL = os.getenv("DOCKER_BOOL", False)
    TEMP_DOWNLOAD_DIR = (
        os.getenv("TEMP_DOWNLOAD_DIR", os.path.abspath("files"))
        if DOCKER_BOOL
        else os.path.abspath("files")
    )
    BROWSER_NAME = os.getenv("BROWSER_NAME", "firefox")
    WINDOW_SIZE = tuple(
        map(int, os.getenv("WINDOW_SIZE", "1280,960").rstrip().split(sep=","))
    )
    EXECUTABLE_PATH = {
        "executable_path": os.getenv("EXECUTABLE_PATH", "/home/lw/bin/geckodriver")
    }
    BASE_URL = os.getenv("BASE_URL", "https://finance.yahoo.com/")
    SEARCH_BAR_XPATH = os.getenv("SEARCH_BAR_XPATH", '//*[@id="yfin-usr-qry"]')
    SEARCH_BUTTON_XPATH = os.getenv(
        "SEARCH_BUTTON_XPATH", '//*[@id="header-desktop-search-button"]'
    )
    HISTORICAL_LINK_XPATH = os.getenv(
        "HISTORICAL_LINK_XPATH", '//*[@id="quote-nav"]/ul/li[6]/a'
    )
    TIME_PERIOD_XPATH = os.getenv(
        "TIME_PERIOD_XPATH",
        '//*[@id="Col1-1-HistoricalDataTable-Proxy"]/section/div[1]/div[1]/div[1]/div/div/div/span',
    )
    TIME_PERIOD_MAX_XPATH = os.getenv(
        "TIME_PERIOD_MAX_XPATH", '//*[@id="dropdown-menu"]/div/ul[2]/li[4]/button'
    )
    HISTORICAL_DATA_DOWNLOAD_XPATH = os.getenv(
        "HISTORICAL_DATA_DOWNLOAD_XPATH",
        '//*[@id="Col1-1-HistoricalDataTable-Proxy"]/section/div[1]/div[2]/span[2]/a',
    )
