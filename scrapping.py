from pyvirtualdisplay import Display
from splinter import Browser
from selenium import webdriver
import splinter
import time
import os
import logging


logging.getLogger().setLevel(logging.INFO)


BASE_URL = "http://www.example.com/"


def yahoo():
    # settings
    browser_name = "firefox"
    browser_window_size = (1280, 960)
    executable_path = {"executable_path": "/home/lw/bin/geckodriver"}
    url = "https://finance.yahoo.com/"
    search_name_company = "DOCU"
    search_bar_xpath = '//*[@id="yfin-usr-qry"]'
    search_button_xpath = '//*[@id="header-desktop-search-button"]'
    historical_link_xpath = '//*[@id="quote-nav"]/ul/li[6]/a'
    time_period_xpath = '//*[@id="Col1-1-HistoricalDataTable-Proxy"]/section/div[1]/div[1]/div[1]/div/div/div/span'
    time_period_max_xpath = '//*[@id="dropdown-menu"]/div/ul[2]/li[4]/button'
    historical_data_download_xpath = (
        '//*[@id="Col1-1-HistoricalDataTable-Proxy"]/section/div[1]/div[2]/span[2]/a'
    )
    prefs = {
        "browser.files.manager.showWhenStarting": "false",
        "browser.helperApps.alwaysAsk.force": "false",
        "browser.files.dir": os.path.abspath("files"), #"/dev/shm", # "os.path.abspath("files")",
        "browser.files.folderList": 2,
        "browser.helperApps.neverAsk.saveToDisk": "text/csv, application/csv, text/html,application/xhtml+xml,application/xml, application/octet-stream, application/pdf, application/x-msexcel,application/excel,application/x-excel,application/excel,application/x-excel,application/excel, application/vnd.ms- excel,application/x-excel,application/x-msexcel,image/png,image/jpeg,text/html,text/plain,application/msword,application/xml,application/excel,text/x-c",
        "browser.files.manager.useWindow": "false",
        "browser.helperApps.useWindow": "false",
        "browser.helperApps.showAlertonComplete": "false",
        "browser.helperApps.alertOnEXEOpen": "false",
        "browser.files.manager.focusWhenStarting": "false",
    }

    # firefox_capabilities = webdriver.DesiredCapabilities.FIREFOX
    # firefox_capabilities["marionette"] = True

    # options = webdriver.FirefoxOptions()
    # firefox_options = webdriver.FirefoxOptions()
    # firefox_options.set_preference("browser.files.manager.showWhenStarting", "false")
    # firefox_options.set_preference("browser.helperApps.alwaysAsk.force", "false")
    # firefox_options.set_preference("browser.files.dir", os.path.abspath("files"))
    # firefox_options.set_preference("browser.files.folderList", 2)
    # firefox_options.set_preference("browser.helperApps.neverAsk.saveToDisk", "text/csv, application/csv, text/html,application/xhtml+xml,application/xml, application/octet-stream, application/pdf, application/x-msexcel,application/excel,application/x-excel,application/excel,application/x-excel,application/excel, application/vnd.ms- excel,application/x-excel,application/x-msexcel,image/png,image/jpeg,text/html,text/plain,application/msword,application/xml,application/excel,text/x-c")
    # firefox_options.set_preference("browser.files.manager.useWindow", "false")
    # firefox_options.set_preference("browser.helperApps.useWindow", "false")
    # firefox_options.set_preference("browser.helperApps.showAlertonComplete", "false")
    # firefox_options.set_preference("browser.helperApps.alertOnEXEOpen", "false")
    # firefox_options.set_preference("browser.files.manager.focusWhenStarting", "false")
    #
    # firefox_options.add_argument("--disable-infobars")

    capabilities_moz = {
        'browserName': 'firefox',
        'marionette': True,
        'acceptInsecureCerts': True,
        'moz:firefoxOptions': {
            'args': [],
            'prefs': {
                # 'network.proxy.type': 1,
                # 'network.proxy.http': '12.157.129.35', 'network.proxy.http_port': 8080,
                # 'network.proxy.ssl':  '12.157.129.35', 'network.proxy.ssl_port':  8080,
                'browser.download.dir': '/dev/shm',
                'browser.helperApps.neverAsk.saveToDisk': "text/csv, application/csv, text/html,application/xhtml+xml,application/xml, application/octet-stream, application/pdf, application/x-msexcel,application/excel,application/x-excel,application/excel,application/x-excel,application/excel, application/vnd.ms- excel,application/x-excel,application/x-msexcel,image/png,image/jpeg,text/html,text/plain,application/msword,application/xml,application/excel,text/x-c",
                'browser.download.useDownloadDir': True,
                'browser.download.manager.showWhenStarting': False,
                'browser.download.animateNotifications': False,
                'browser.safebrowsing.downloads.enabled': False,
                'browser.download.folderList': 2,
                'pdfjs.disabled': True
            }
        }
    }
    # display = Display(visible=0, size=(800, 600))
    # display.start()

    # driver = webdriver.Firefox(capabilities=firefox_capabilities, firefox_profile=fp)
    # browser = Browser(browser_name, profile_preferences=prefs, **executable_path)
    # web_driver = webdriver.Remote(
    #     "http://localhost:4444/",
    #     desired_capabilities=webdriver.DesiredCapabilities.CHROME)

    remote_server_url = 'http://localhost:4444/wd/hub'

    # prefs = {
    #     "download.default_directory": "/dev/shm",
    #     "download.directory_upgrade": "true",
    #     "download.prompt_for_download": "false",
    #     "disable-popup-blocking": "true"
    #
    # }
    print(prefs)
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_experimental_option("prefs", prefs)
    chrome_options.add_argument("--disable-infobars")
    # browser = splinter.Browser('chrome', options=chrome_options)

    # with Browser(
    #         # # driver_name="remote",
    #         # browser='firefox',
    #         # # command_executor=remote_server_url,
    #         # keep_alive=True,
    #         # options=firefox_options
    #         browser_name, profile_preferences=prefs, **executable_path
    # ) as browser:
    browser = Browser(browser_name, profile_preferences=prefs, **executable_path)
    browser.driver.set_window_size(*browser_window_size)
    browser.visit(url)
    search_bar = browser.find_by_xpath(search_bar_xpath)[0]
    search_bar.fill(search_name_company)
    time.sleep(1)
    search_button = browser.find_by_xpath(search_button_xpath)[0]
    search_button.click()
    historical_link = browser.find_by_xpath(historical_link_xpath)[0]
    historical_link.click()
    time_period = browser.find_by_xpath(time_period_xpath)[0]
    time_period.click()
    time_period_max = browser.find_by_xpath(time_period_max_xpath)[0]
    time_period_max.click()
    print(browser.html)
    historical_data_download = browser.find_by_xpath(historical_data_download_xpath)[0]
    historical_data_download.click()
    # browser.close()


yahoo()
