from splinter import Browser
from selenium import webdriver
import settings
import time
import logging


logging.getLogger().setLevel(logging.INFO)


BASE_URL = "http://www.example.com/"


class YahooFinScrap:
    def __init__(self, search_name_company):
        self.search_name_company = search_name_company
        self.__settings_env__(self)
        # self.__execute_with_browser__()
        self.__execute_with_docker__()

    @staticmethod
    def __settings_env__(self):
        self.browser_name = settings.BROWSER_NAME
        self.browser_window_size = settings.WINDOW_SIZE
        self.executable_path = settings.EXECUTABLE_PATH
        self.url = settings.BASE_URL
        self.search_bar_xpath = settings.SEARCH_BAR_XPATH
        self.search_button_xpath = settings.SEARCH_BUTTON_XPATH
        self.historical_link_xpath = settings.HISTORICAL_LINK_XPATH
        self.time_period_xpath = settings.TIME_PERIOD_XPATH
        self.time_period_max_xpath = settings.TIME_PERIOD_MAX_XPATH
        self.historical_data_download_xpath = settings.HISTORICAL_DATA_DOWNLOAD_XPATH
        self.temp_download_dir = settings.TEMP_DOWNLOAD_DIR

    @staticmethod
    def __browser_prefs__(browser_name, download_dir):
        firefox_prefs = {
            "browser.download.manager.showWhenStarting": "false",
            "browser.helperApps.alwaysAsk.force": "false",
            "browser.download.dir": download_dir,
            "browser.download.folderList": 2,
            "browser.helperApps.neverAsk.saveToDisk": "text/csv, application/csv, text/html,application/xhtml+xml,application/xml, application/octet-stream, application/pdf, application/x-msexcel,application/excel,application/x-excel,application/excel,application/x-excel,application/excel, application/vnd.ms- excel,application/x-excel,application/x-msexcel,image/png,image/jpeg,text/html,text/plain,application/msword,application/xml,application/excel,text/x-c",
            "browser.download.manager.useWindow": "false",
            "browser.helperApps.useWindow": "false",
            "browser.helperApps.showAlertonComplete": "false",
            "browser.helperApps.alertOnEXEOpen": "false",
            "browser.download.manager.focusWhenStarting": "false",
        }
        chrome_prefs = {
            "download.default_directory": download_dir,
            "download.directory_upgrade": "true",
            "download.prompt_for_download": "false",
            "disable-popup-blocking": "true",
        }
        if browser_name == "firefox":
            return firefox_prefs
        elif browser_name == "chrome":
            return chrome_prefs
        else:
            return None

    @staticmethod
    def __browser_options__(self):
        # Chrome options
        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_experimental_option(
            "prefs", self.__browser_prefs__(self.browser_name, self.temp_download_dir)
        )
        chrome_options.add_argument("--disable-infobars")

        # Firefox options
        firefox_options = webdriver.FirefoxOptions()
        firefox_options.set_preference(
            "browser.files.manager.showWhenStarting", "false"
        )
        firefox_options.set_preference("browser.helperApps.alwaysAsk.force", "false")
        firefox_options.set_preference("browser.files.dir", self.temp_download_dir)
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

        if self.browser_name == "firefox":
            return firefox_options
        elif self.browser_name == "chrome":
            return chrome_options
        else:
            return None

    @staticmethod
    def __capabilities_mozilla__(download_dir):
        firefox_capabilities = webdriver.DesiredCapabilities.FIREFOX
        firefox_capabilities["marionette"] = True

        firefox_capabilities = {
            "browserName": "firefox",
            "marionette": True,
            "acceptInsecureCerts": True,
            "moz:firefoxOptions": {
                "args": [],
                "prefs": {
                    # 'network.proxy.type': 1,
                    # 'network.proxy.http': '12.157.129.35', 'network.proxy.http_port': 8080,
                    # 'network.proxy.ssl':  '12.157.129.35', 'network.proxy.ssl_port':  8080,
                    "browser.download.dir": download_dir,
                    "browser.helperApps.neverAsk.saveToDisk": "text/csv, application/csv, text/html,application/xhtml+xml,application/xml, application/octet-stream, application/pdf, application/x-msexcel,application/excel,application/x-excel,application/excel,application/x-excel,application/excel, application/vnd.ms- excel,application/x-excel,application/x-msexcel,image/png,image/jpeg,text/html,text/plain,application/msword,application/xml,application/excel,text/x-c",
                    "browser.download.useDownloadDir": True,
                    "browser.download.manager.showWhenStarting": False,
                    "browser.download.animateNotifications": False,
                    "browser.safebrowsing.downloads.enabled": False,
                    "browser.download.folderList": 2,
                    "pdfjs.disabled": True,
                },
            },
        }
        return firefox_capabilities

    def __execute_with_browser__(self):
        if self.browser_name == "firefox":
            firefox_capabilities = webdriver.DesiredCapabilities.FIREFOX
            firefox_capabilities["marionette"] = True
            with Browser(
                self.browser_name,
                # profile_preferences=self.__browser_prefs__(self.browser_name, self.temp_download_dir),
                options=self.__browser_options__(self),
                **self.executable_path
            ) as browser:
                self.__yahoo_scrapping__(self, browser)
        else:
            print("Implemented only Firefox")

    def __execute_with_docker__(self):
        remote_server_url = "http://localhost:4444/wd/hub"
        with Browser(
            driver_name="remote",
            browser=self.browser_name,
            command_executor=remote_server_url,
            keep_alive=True,
            options=self.__browser_options__(self),
        ) as browser:
            self.__yahoo_scrapping__(self, browser)

    @staticmethod
    def __yahoo_scrapping__(self, browser):
        browser.driver.set_window_size(*self.browser_window_size)
        browser.visit(self.url)
        search_bar = browser.find_by_xpath(self.search_bar_xpath)[0]
        search_bar.fill(self.search_name_company)
        time.sleep(1)
        search_button = browser.find_by_xpath(self.search_button_xpath)[0]
        search_button.click()
        historical_link = browser.find_by_xpath(self.historical_link_xpath)[0]
        historical_link.click()
        time_period = browser.find_by_xpath(self.time_period_xpath)[0]
        time_period.click()
        time_period_max = browser.find_by_xpath(self.time_period_max_xpath)[0]
        time_period_max.click()
        print(browser.html)
        historical_data_download = browser.find_by_xpath(
            self.historical_data_download_xpath
        )[0]
        historical_data_download.click()


YahooFinScrap(search_name_company="DOCU")
