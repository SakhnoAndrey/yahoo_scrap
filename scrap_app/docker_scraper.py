from .base_scraper import BaseScraper
from splinter import Browser


class DockerScraper(BaseScraper):
    def create_browser(self) -> Browser:
        remote_server_url = "http://localhost:4444/wd/hub"
        if self.config.BROWSER_NAME == "firefox":
            firefox_preferences = self._browser_prefs(config=self.config)
            browser = Browser(
                driver_name="remote",
                browser=self.config.BROWSER_NAME,
                command_executor=remote_server_url,
                keep_alive=True,
                profile_preferences=firefox_preferences,
            )
            return browser
        elif self.config.BROWSER_NAME == "chrome":
            chrome_options = self._browser_options(
                config=self.config, prefs=self._browser_prefs(config=self.config)
            )
            browser = Browser(
                driver_name="remote",
                browser=self.config.BROWSER_NAME,
                command_executor=remote_server_url,
                keep_alive=True,
                options=chrome_options,
            )
            return browser
        else:
            print("Not implemented to this browser")
            return None
