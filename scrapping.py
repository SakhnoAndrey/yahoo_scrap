from splinter import Browser
import splinter
import time
from selenium import webdriver

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
browser = Browser(browser_name, **executable_path)  # options=firefox_options,
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
