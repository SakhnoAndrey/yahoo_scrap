from splinter import Browser
from selenium import webdriver
from settings import ConfigBase
import time
import logging


logging.getLogger().setLevel(logging.INFO)


BASE_URL = "http://www.example.com/"


class BaseScraper:

    config = ConfigBase()
    browser = Browser()

    def __init__(self):
        # self.__execute_with_browser__()
        self.__execute_with_docker__()

    @staticmethod
    def _browser_prefs(config: ConfigBase):
        firefox_prefs = {
            "browser.download.manager.showWhenStarting": "false",
            "browser.helperApps.alwaysAsk.force": "false",
            "browser.download.dir": config.TEMP_DOWNLOAD_DIR,
            "browser.download.folderList": 2,
            "browser.helperApps.neverAsk.saveToDisk": "text/csv, application/csv, text/html,application/xhtml+xml,application/xml, application/octet-stream, application/pdf, application/x-msexcel,application/excel,application/x-excel,application/excel,application/x-excel,application/excel, application/vnd.ms- excel,application/x-excel,application/x-msexcel,image/png,image/jpeg,text/html,text/plain,application/msword,application/xml,application/excel,text/x-c",
            "browser.download.manager.useWindow": "false",
            "browser.helperApps.useWindow": "false",
            "browser.helperApps.showAlertonComplete": "false",
            "browser.helperApps.alertOnEXEOpen": "false",
            "browser.download.manager.focusWhenStarting": "false",
        }
        chrome_prefs = {
            "download.default_directory": config.TEMP_DOWNLOAD_DIR,
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
    def _browser_options(config: ConfigBase, prefs):
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
        firefox_options.set_preference("browser.files.dir", config.TEMP_DOWNLOAD_DIR)
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
    def _capabilities_mozilla(config: ConfigBase):
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
                    "browser.download.dir": config.TEMP_DOWNLOAD_DIR,
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

    """
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
    """

    def feth_data_for(self, company_name):
        self.browser.driver.set_window_size(*self.config.WINDOW_SIZE)
        self.browser.visit(self.config.BASE_URL)
        search_bar = self.browser.find_by_xpath(self.config.SEARCH_BAR_XPATH)[0]
        search_bar.fill(company_name)
        time.sleep(1)
        search_button = self.browser.find_by_xpath(self.config.SEARCH_BUTTON_XPATH)[0]
        search_button.click()
        historical_link = self.browser.find_by_xpath(self.config.HISTORICAL_LINK_XPATH)[
            0
        ]
        historical_link.click()
        time_period = self.browser.find_by_xpath(self.config.TIME_PERIOD_XPATH)[0]
        time_period.click()
        time_period_max = self.browser.find_by_xpath(self.config.TIME_PERIOD_MAX_XPATH)[
            0
        ]
        time_period_max.click()
        print(self.browser.html)
        historical_data_download = self.browser.find_by_xpath(
            self.config.HISTORICAL_DATA_DOWNLOAD_XPATH
        )[0]
        historical_data_download.click()

    def __del__(self):
        self.browser.quit()


class DockerScraper(BaseScraper):
    def __init__(self):
        remote_server_url = "http://localhost:4444/wd/hub"
        self.browser = Browser(
            driver_name="remote",
            browser=self.config.BROWSER_NAME,
            command_executor=remote_server_url,
            keep_alive=True,
            options=self._browser_options(
                config=self.config, prefs=self._browser_prefs(self.config)
            ),
        )
        super().__init__()


class BrowserScraper(BaseScraper):
    def __init__(self):
        if self.config.BROWSER_NAME == "firefox":
            firefox_capabilities = webdriver.DesiredCapabilities.FIREFOX
            firefox_capabilities["marionette"] = True
            self.browser = Browser(
                self.config.BROWSER_NAME,
                # profile_preferences=self.__browser_prefs__(self.browser_name, self.temp_download_dir),
                options=self._browser_options(
                    config=self.config, prefs=self._browser_prefs(self.config)
                ),
                **self.config.EXECUTABLE_PATH
            )
        else:
            print("Implemented only Firefox")
        super().__init__()


# YahooFinScrap(search_name_company="DOCU")
if ConfigBase.DOCKER_BOOL:
    # scraper = DockerScraper()
    # scraper.feth_data_for(company_name="DOCU")
    pass
else:
    # scraper = BrowserScraper()
    print("browser")
    # scraper.feth_data_for(company_name="DOCU")
