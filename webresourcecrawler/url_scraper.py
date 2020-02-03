import os

from selenium import webdriver
import urllib.request
import platform
from textwrap import dedent
from shutil import which


class UrlScraper:
    def __init__(self, chrome_driver_path=None):
        self.chrome_driver_path = chrome_driver_path if chrome_driver_path else 'chromedriver'
        self.chrome_driver_path = self._check_chrome_driver()

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
        options = webdriver.ChromeOptions()
        options.add_argument('--headless')
        options.add_argument('--disable-extensions')
        options.add_argument('--disable-gpu')
        options.add_argument("--no-sandbox")
        options.add_argument('--disable-dev-shm-usage')
        options.add_argument('--disable-browser-side-navigation')
        options.add_argument('--log-level=3')
        browser = webdriver.Chrome(options=options, executable_path=self.chrome_driver_path)
        try:
            browser.get(url)
        finally:
            html = browser.page_source
            browser.quit()
        return html

    def _check_chrome_driver(self):
        has_chrome_driver_in_path = which(self.chrome_driver_path)
        if has_chrome_driver_in_path is not None:
            return self.chrome_driver_path
        else:
            if platform.system() == 'Windows':
                _here = os.path.abspath(os.path.dirname(__file__))
                default_windows_path = os.path.join(_here, 'chromedriver.exe')
                if os.path.exists(default_windows_path):
                    return default_windows_path
                raise FileNotFoundError(dedent("""\
                    chromedriver is not available in PATH.
                    Pull the branch down again, or download it to your PATH:
                    https://chromedriver.chromium.org/downloads
                    """))
            if platform.system() == 'Darwin':
                raise FileNotFoundError(dedent("""\
                chromedriver is not available in PATH.
                Install it using homebrew and try again:
                $ brew cask install chromedriver
                """))
