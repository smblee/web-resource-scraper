import os
from selenium import webdriver
import urllib.request
import platform
from textwrap import dedent


class UrlScraper:
    def __init__(self, mac_headless_path=None, windows_headless_path=None):
        _here = os.path.abspath(os.path.dirname(__file__))
        self.mac_headless_path = mac_headless_path if mac_headless_path else \
            r'/Applications/Google Chrome Canary.app' \
            r'/Contents/MacOS/Google Chrome Canary'
        self.windows_headless_path = windows_headless_path if windows_headless_path else \
            os.path.join(_here, 'chromedriver.exe')
        self.headless_path = self._check_selenium_compatibility()

    def fetch_url_html_with_get(self, url):
        request_headers = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_3)'
                          'AppleWebKit/537.36 (KHTML, like Gecko) '
                          'Chrome/35.0.1916.47 Safari/537.36 '
        }
        req = urllib.request.Request(url, data=None, headers=request_headers)

        try:
            with urllib.request.urlopen(req) as response:
                html = response.read().decode()
                return html
        except urllib.request.HTTPError:
            return None
        except UnicodeDecodeError:
            return None

    def fetch_url_html_with_selenium(self, url):
        chromedriver = self.headless_path
        options = webdriver.ChromeOptions()
        options.add_argument('--headless')
        options.add_argument('--disable-extensions')
        options.add_argument('--disable-gpu')
        options.add_argument("--no-sandbox")
        options.add_argument('--disable-dev-shm-usage')
        options.add_argument('--disable-browser-side-navigation')
        browser = webdriver.Chrome(options=options)
        try:
            browser.get(url)
        finally:
            html = browser.page_source
            browser.quit()
        return html

    def _check_selenium_compatibility(self):
        if platform.system() == 'Windows':
            if not os.path.exists(self.windows_headless_path):
                raise FileNotFoundError(dedent("""\
                    Chrome Headless browser is not installed.
                    Install them by pulling the branch (the file should be included in git)
                    """))
            return self.windows_headless_path

        if platform.system() == 'Darwin':
            if not os.path.exists(self.mac_headless_path):
                raise FileNotFoundError(dedent("""\
                    Chrome Headless browser is not installed.
                    Install them using homebrew:
                    $ brew cask install chromedriver
                    $ brew install Caskroom/versions/google-chrome-canary
                    """))
            return self.mac_headless_path
        raise NotImplementedError(
            "use_selenium option is only supported for Windows/Mac platforms currently." +
            "Crawling SPA via Selenium is not supported on this platform.")
