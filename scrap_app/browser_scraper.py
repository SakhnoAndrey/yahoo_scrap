from .base_scraper import BaseScraper
from splinter import Browser


class BrowserScraper(BaseScraper):
    def create_browser(self) -> Browser:
        if self.config.BROWSER_NAME == "firefox":
            firefox_preferences = self._browser_prefs(config=self.config)
            browser = Browser(
                self.config.BROWSER_NAME,
                profile_preferences=firefox_preferences,
                **self.config.EXECUTABLE_PATH
            )
            return browser
        elif self.config.BROWSER_NAME == "chrome":
            chrome_options = self._browser_options(
                config=self.config, prefs=self._browser_prefs(config=self.config)
            )
            browser = Browser(self.config.BROWSER_NAME, options=chrome_options)
            return browser
        else:
            print("Not implemented to this browser")
            return None
