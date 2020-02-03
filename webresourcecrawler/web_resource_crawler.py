from .resource_gatherer import ResourceGatherer
from .url_utils import UrlUtils
from .url_scraper import UrlScraper

import json
from bs4 import BeautifulSoup
import tldextract
from queue import Queue, Empty
from concurrent.futures import ThreadPoolExecutor, wait
from urllib.parse import urlparse


class WebResourceCrawler:
    def __init__(
            self,
            url,
            chrome_driver_path=None,
            ignore_alternate_rel=True,
            worker_count=6,
            worker_timeout_s=20):
        self.url = url
        self.root_url = '{}://{}'.format(urlparse(self.url).scheme,
                                         urlparse(self.url).netloc)
        self.pool = ThreadPoolExecutor(max_workers=worker_count)
        self.workers = []
        self.processed_urls = set()
        self.queue = Queue()
        self.worker_timeout_s = worker_timeout_s
        self.url_scraper = UrlScraper(chrome_driver_path)
        self.ignore_alternate_rel = ignore_alternate_rel
        self.resource_gatherer = ResourceGatherer(urlparse(self.url).netloc)

    def run(self, get_only_best_resources=True, use_selenium=False, retry=True):
        # reset the instances in case this is not the first run
        self._reset_instance()
        self._run_scraper_parallel(use_selenium)
        wait(self.workers)
        print("Gathering results...")
        results = self._get_scraped_resources(get_only_best_resources)
        if not results:
            if retry and not use_selenium:
                print(
                    "Did not find any resources."
                    "Trying headless browser with selenium in case"
                    "the website is a SPA (React, Vue, etc.).")

                return self.run(
                    use_selenium=True,
                    get_only_best_resources=get_only_best_resources,
                    retry=False)
            else:
                print(
                    "did not find any resources. Try increasing `worker_timeout_s` if timed out.")

        return json.dumps(results, indent=4)

    def _reset_instance(self):
        self.workers = []
        self.processed_urls = set()
        ext = tldextract.extract(self.url)
        if not ext.domain or not self._try_add_to_queue(self.url):
            raise ValueError(
                f"Failed to initialize WebResourceCrawler." +
                f"'url' ({self.url}) was either incorrectly formed or failed to fetch.")

    def _run_scraper_parallel(self, use_selenium=False):
        while True:
            try:
                current_url = self.queue.get(timeout=self.worker_timeout_s)
                if current_url in self.processed_urls:
                    continue
                self.processed_urls.add(current_url)
                job = self.pool.submit(
                    self._process_url, current_url, use_selenium)
                self.workers.append(job)
            except Empty:
                print(
                    f"Queue timed out after {self.worker_timeout_s} seconds.")
                return
            except Exception as e:
                print(e)
                continue

    def _parse_urls_from_html(self, html):
        soup = BeautifulSoup(html, 'html.parser')
        links = soup.find_all(href=True)

        return [(link['href'], link) for link in links]

    def _try_add_to_queue(self, url, html_tag=None):
        # ignore if the url is malformed
        absolute_url = UrlUtils.get_absolute_url(self.root_url, url)

        # ignore this url if it's None or has been processed before.
        if not absolute_url or absolute_url in self.processed_urls:
            return False

        # # perform html tag related checks.
        # if html_tag and self.ignore_alternate_rel and 'alternates' in html_tag['rel']:
        #     return False

        if UrlUtils.has_same_domain(absolute_url, self.root_url):
            self.queue.put(absolute_url)
            return True

        return False

    def _get_scraped_resources(self, get_only_best_resources):
        return self.resource_gatherer.get_gathered_resources(get_only_best_resources)

    def _process_url(self, url, with_selenium=False):
        print(
            f"Processing URL: {url} " +
            f"({'can be slow due to headless browser method' if with_selenium else 'GET mode'})")
        url_html = self.url_scraper.fetch_url_html_with_get(url) if not with_selenium \
            else self.url_scraper.fetch_url_html_with_selenium(url)
        if url_html:
            neighbor_urls_and_tags = self._parse_urls_from_html(url_html)
            for neighbor_url, neighbor_href_tag in neighbor_urls_and_tags:
                self._try_add_to_queue(neighbor_url, neighbor_href_tag)
                self.resource_gatherer.feed_url(neighbor_url)
