from splinter import Browser
import csv
import glob
import json
import os
import time
from abc import abstractmethod
from bs4 import BeautifulSoup
from selenium import webdriver
from splinter.exceptions import ElementDoesNotExist
from rest_app.services import save_company_data


class BaseScraper:
    def __init__(self, config):
        self.config = config

    @abstractmethod
    def create_browser(self) -> Browser:
        pass

    @staticmethod
    def _browser_prefs(config):
        firefox_prefs = {
            "browser.download.manager.showWhenStarting": "false",
            "browser.helperApps.alwaysAsk.force": "false",
            "browser.download.dir": config.DOWNLOAD_DIR_BROWSER,
            "browser.download.folderList": 2,
            "browser.helperApps.neverAsk.saveToDisk": "text/csv, application/csv, text/html,application/xhtml+xml,application/xml, application/octet-stream, application/pdf, application/x-msexcel,application/excel,application/x-excel,application/excel,application/x-excel,application/excel, application/vnd.ms- excel,application/x-excel,application/x-msexcel,image/png,image/jpeg,text/html,text/plain,application/msword,application/xml,application/excel,text/x-c",
            "browser.download.manager.useWindow": "false",
            "browser.helperApps.useWindow": "false",
            "browser.helperApps.showAlertonComplete": "false",
            "browser.helperApps.alertOnEXEOpen": "false",
            "browser.download.manager.focusWhenStarting": "false",
        }
        chrome_prefs = {
            "download.default_directory": config.DOWNLOAD_DIR_BROWSER,
            "download.directory_upgrade": "true",
            "download.prompt_for_download": "false",
            "disable-popup-blocking": "true",
        }
        if config.BROWSER_NAME == "firefox":
            return firefox_prefs
        elif config.BROWSER_NAME == "chrome":
            return chrome_prefs
        else:
            return None

    @staticmethod
    def _browser_options(config, prefs):
        # Chrome options
        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_experimental_option("prefs", prefs)
        chrome_options.add_argument("--disable-infobars")

        # Firefox options
        firefox_options = webdriver.FirefoxOptions()
        firefox_options.set_preference(
            "browser.files.manager.showWhenStarting", "false"
        )
        firefox_options.set_preference("browser.helperApps.alwaysAsk.force", "false")
        firefox_options.set_preference("browser.files.dir", config.DOWNLOAD_DIR_BROWSER)
        firefox_options.set_preference("browser.files.folderList", 2)
        firefox_options.set_preference(
            "browser.helperApps.neverAsk.saveToDisk",
            "text/csv, application/csv, text/html,application/xhtml+xml,application/xml, application/octet-stream, application/pdf, application/x-msexcel,application/excel,application/x-excel,application/excel,application/x-excel,application/excel, application/vnd.ms- excel,application/x-excel,application/x-msexcel,image/png,image/jpeg,text/html,text/plain,application/msword,application/xml,application/excel,text/x-c",
        )
        firefox_options.set_preference("browser.files.manager.useWindow", "false")
        firefox_options.set_preference("browser.helperApps.useWindow", "false")
        firefox_options.set_preference(
            "browser.helperApps.showAlertonComplete", "false"
        )
        firefox_options.set_preference("browser.helperApps.alertOnEXEOpen", "false")
        firefox_options.set_preference(
            "browser.files.manager.focusWhenStarting", "false"
        )
        firefox_options.add_argument("--disable-infobars")

        if config.BROWSER_NAME == "firefox":
            return firefox_options
        elif config.BROWSER_NAME == "chrome":
            return chrome_options
        else:
            return None

    @staticmethod
    def _capabilities_mozilla(config):
        firefox_capabilities = webdriver.DesiredCapabilities.FIREFOX
        firefox_capabilities["marionette"] = True

        firefox_capabilities = {
            "browserName": "firefox",
            "marionette": True,
            "acceptInsecureCerts": True,
            "moz:firefoxOptions": {
                "args": [],
                "prefs": {
                    "browser.download.dir": config.DOWNLOAD_DIR_BROWSER,
                    "browser.helperApps.neverAsk.saveToDisk": "text/csv, application/csv, text/html,application/xhtml+xml,application/xml, application/octet-stream, application/pdf, application/x-msexcel,application/excel,application/x-excel,application/excel,application/x-excel,application/excel, application/vnd.ms- excel,application/x-excel,application/x-msexcel,image/png,image/jpeg,text/html,text/plain,application/msword,application/xml,application/excel,text/x-c",
                    "browser.download.useDownloadDir": "true",
                    "browser.download.manager.showWhenStarting": "false",
                    "browser.download.animateNotifications": "false",
                    "browser.safebrowsing.downloads.enabled": "false",
                    "browser.download.folderList": 2,
                    "pdfjs.disabled": "true",
                    "browser.helperApps.alwaysAsk.force": "false",
                    "browser.download.manager.useWindow": "false",
                    "browser.helperApps.useWindow": "false",
                    "browser.helperApps.showAlertonComplete": "false",
                    "browser.helperApps.alertOnEXEOpen": "false",
                    "browser.download.manager.focusWhenStarting": "false",
                },
            },
        }
        return firefox_capabilities

    @staticmethod
    def _create_folder(folder):
        # Create missing downloaded images and goal folders
        access_rights = 0o755
        try:
            if not os.path.exists(os.path.abspath(folder)):
                os.makedirs(os.path.abspath(folder), access_rights)
        except OSError:
            print("Create directory %s failed" % os.path.abspath(folder))

    @staticmethod
    def _html_to_file(self, html):
        # Download html file needed page of site (not uses, only for test)
        self._create_folder("files")
        with open(
            os.path.join(os.path.abspath("files"), "orders.html"), "w"
        ) as goal_file:
            soup = BeautifulSoup(html, "lxml")
            content = soup.prettify(formatter="html5")
            goal_file.write(content)

    def fetch_data_for(self, company_names):
        with self.create_browser() as browser:
            browser.driver.set_window_size(*self.config.WINDOW_SIZE)
            for company_name in company_names:
                print("Scraping data for company {0}".format(company_name))
                browser.visit(self.config.BASE_URL)
                search_bar = browser.find_by_xpath(self.config.SEARCH_BAR_XPATH)[0]
                search_bar.fill(company_name)
                time.sleep(1)
                search_button = browser.find_by_xpath(self.config.SEARCH_BUTTON_XPATH)[
                    0
                ]
                search_button.click()
                try:
                    historical_link = browser.find_by_xpath(
                        self.config.HISTORICAL_LINK_XPATH
                    )[0]
                    historical_link.click()
                    time_period = browser.find_by_xpath(self.config.TIME_PERIOD_XPATH)[
                        0
                    ]
                    time_period.click()
                    time_period_max = browser.find_by_xpath(
                        self.config.TIME_PERIOD_MAX_XPATH
                    )[0]
                    time_period_max.click()
                    self._html_to_file(self, browser.html)
                    historical_data_download = browser.find_by_xpath(
                        self.config.HISTORICAL_DATA_DOWNLOAD_XPATH
                    )[0]
                    historical_data_download.click()
                    time.sleep(20)
                    json_data = self._last_csv_to_json()
                    save_company_data(name=company_name, data=json_data)
                    print("Download data file for company {0}".format(company_name))
                except ElementDoesNotExist:
                    print("Company {0} not found".format(company_name))

    def _last_csv_to_json(self) -> list:
        list_files = glob.glob(os.path.join(self.config.DOWNLOAD_DIR_MACHINE, "*.csv"))
        latest_file = max(list_files, key=os.path.getctime)
        with open(latest_file, "r") as f:
            csv_reader = csv.DictReader(f)
            json_array = [row for row in csv_reader]
            json_string = json.dumps(json_array, indent=4)
            return json_string
