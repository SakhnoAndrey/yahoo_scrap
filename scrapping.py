from splinter import Browser
from selenium import webdriver
from settings import ConfigBase
import time
import logging
from abc import abstractmethod


logging.getLogger().setLevel(logging.INFO)


BASE_URL = "http://www.example.com/"


class BaseScraper:
    def __init__(self, config):
        self.config = config
        pass

    @abstractmethod
    def create_browser(self) -> Browser:
        pass

    @staticmethod
    def _browser_prefs(config):
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

    def fetch_data_for(self, company_name):
        with self.create_browser() as browser:
            browser.driver.set_window_size(*self.config.WINDOW_SIZE)
            browser.visit(self.config.BASE_URL)
            search_bar = browser.find_by_xpath(self.config.SEARCH_BAR_XPATH)[0]
            search_bar.fill(company_name)
            time.sleep(1)
            search_button = browser.find_by_xpath(self.config.SEARCH_BUTTON_XPATH)[0]
            search_button.click()
            historical_link = browser.find_by_xpath(self.config.HISTORICAL_LINK_XPATH)[
                0
            ]
            historical_link.click()
            time_period = browser.find_by_xpath(self.config.TIME_PERIOD_XPATH)[0]
            time_period.click()
            time_period_max = browser.find_by_xpath(self.config.TIME_PERIOD_MAX_XPATH)[
                0
            ]
            time_period_max.click()
            print(browser.html)
            historical_data_download = browser.find_by_xpath(
                self.config.HISTORICAL_DATA_DOWNLOAD_XPATH
            )[0]
            historical_data_download.click()


class DockerScraper(BaseScraper):
    def create_browser(self) -> Browser:
        remote_server_url = "http://localhost:4444/wd/hub"
        browser = Browser(
            driver_name="remote",
            browser=self.config.BROWSER_NAME,
            command_executor=remote_server_url,
            keep_alive=True,
            options=self._browser_options(
                config=self.config, prefs=self._browser_prefs(self.config)
            ),
        )
        return browser


class BrowserScraper(BaseScraper):
    def create_browser(self) -> Browser:
        if self.config.BROWSER_NAME == "firefox":
            firefox_capabilities = webdriver.DesiredCapabilities.FIREFOX
            firefox_capabilities["marionette"] = True
            browser = Browser(
                self.config.BROWSER_NAME,
                # profile_preferences=self.__browser_prefs__(self.browser_name, self.temp_download_dir),
                options=self._browser_options(
                    config=self.config, prefs=self._browser_prefs(self.config)
                ),
                **self.config.EXECUTABLE_PATH
            )
            return browser
        else:
            print("Implemented only Firefox")
            return None


if __name__ == "__main__":
    config = ConfigBase()
    company_name = "DOCU"
    if config.DOCKER_BOOL:
        scraper = DockerScraper(config)
    else:
        scraper = BrowserScraper(config)
    scraper.fetch_data_for(company_name=company_name)
