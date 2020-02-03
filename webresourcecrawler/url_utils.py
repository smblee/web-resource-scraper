import tldextract
from urllib.parse import urljoin
from validator_collection import checkers


class UrlUtils:
    @staticmethod
    def has_same_domain(url_1, url_2):
        extracted_url_1 = tldextract.extract(url_1)
        extracted_url_2 = tldextract.extract(url_2)
        return extracted_url_1.domain == extracted_url_2.domain

    @staticmethod
    def get_absolute_url(root_url, url):
        # convert relative URL to absolute URL
        if url.startswith('/'):
            return urljoin(root_url, url)
        if not checkers.is_url(url):
            return None
        return url
