from pyvirtualdisplay import Display
from splinter import Browser
from selenium import webdriver
import splinter
import time
import os
import logging


logging.getLogger().setLevel(logging.INFO)


BASE_URL = "http://www.example.com/"


def chrome_example():
    display = Display(visible=0, size=(800, 600))
    display.start()
    logging.info("Initialized virtual display..")

    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument("--no-sandbox")

    chrome_options.add_experimental_option(
        "prefs",
        {
            "download.default_directory": os.getcwd(),
            "download.prompt_for_download": False,
        },
    )
    logging.info("Prepared chrome options..")

    # browser = webdriver.Chrome(chrome_options=chrome_options)
    web_driver = webdriver.Remote(
        command_executor="localhost:4444",
        desired_capabilities=webdriver.DesiredCapabilities.CHROME,
    )
    browser = webdriver.Chrome(chrome_options=chrome_options)
    logging.info("Initialized chrome browser..")

    browser.get(BASE_URL)
    logging.info("Accessed %s ..", BASE_URL)

    logging.info("Page title: %s", browser.title)

    browser.quit()
    display.stop()


def firefox_example():
    display = Display(visible=0, size=(800, 600))
    display.start()
    logging.info("Initialized virtual display..")

    firefox_profile = webdriver.FirefoxProfile()
    firefox_profile.set_preference("browser.download.folderList", 2)
    firefox_profile.set_preference("browser.download.manager.showWhenStarting", False)
    firefox_profile.set_preference("browser.download.dir", os.getcwd())
    firefox_profile.set_preference("browser.helperApps.neverAsk.saveToDisk", "text/csv")

    logging.info("Prepared firefox profile..")

    browser = webdriver.Firefox(firefox_profile=firefox_profile)
    logging.info("Initialized firefox browser..")

    browser.get(BASE_URL)
    logging.info("Accessed %s ..", BASE_URL)

    logging.info("Page title: %s", browser.title)

    browser.quit()
    display.stop()


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
        "download.default_directory": "C:/Users/joshuaclew/Downloads/",
        "download.directory_upgrade": "true",
        "download.prompt_for_download": "false",
        "disable-popup-blocking": "true",
    }

    # options = webdriver.FirefoxOptions()
    # firefox_options = webdriver.FirefoxOptions()
    # options.set_preference("prefs", prefs)
    # firefox_options.add_argument("--disable-infobars")
    # display = Display(visible=0, size=(800, 600))
    # display.start()

    browser = Browser(browser_name, **executable_path)  # options=firefox_options
    # web_driver = webdriver.Remote(
    #     "http://localhost:4444/",
    #     desired_capabilities=webdriver.DesiredCapabilities.CHROME)

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
    historical_data_download = browser.find_by_xpath(historical_data_download_xpath)[0]
    historical_data_download.click()

    # search_company_xpath = '//*[@id="quote-header-info"]/div[2]/div[1]/div[1]/h1'
    # search_company = browser.find_by_xpath(search_company_xpath)[0]
    # print(search_company.text.encode('utf8'))
    # browser.close()


chrome_example()
