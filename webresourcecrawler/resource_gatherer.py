from functools import cmp_to_key
from fuzzywuzzy import fuzz
import re


class ResourceGatherer:
    def __init__(self, keyword=""):
        self.ios_regex = r"^https?://apps.apple.com/.*/?app/.*/id(\d+)"
        self.twitter_regex = r"^https?://twitter.com/([A-Za-z0-9\_]+)"
        self.google_regex = r"^https?://play\.google\.com/store/apps.*id=([^&]*)"
        self.facebook_regex = r"^https?://(?:www\.)?facebook\.com/(\d+|[A-Za-z0-9\.]+)/?"
        self.ios = set()
        self.twitter = set()
        self.google = set()
        self.facebook = set()
        self.supported_resources = {"ios": (self.ios, self._handle_ios),
                                    "twitter": (self.twitter, self._handle_twitter),
                                    "google": (self.google, self._handle_google),
                                    "facebook": (self.facebook, self._handle_facebook)}
        self.keyword_for_fuzzy_sort = keyword.lower()

    def feed_url(self, url):
        for gathered_resource_set, handle_fn in self.supported_resources.values():
            res = handle_fn(url)
            if res:
                gathered_resource_set.add(res)

    def _handle_with_regex(self, url, pattern):
        res = re.search(pattern, url)

        if not res or not res.group(1):
            return None

        return res.group(1)

    def _handle_facebook(self, url):
        return self._handle_with_regex(url, self.facebook_regex)

    def _handle_google(self, url):
        return self._handle_with_regex(url, self.google_regex)

    def _handle_twitter(self, url):
        return self._handle_with_regex(url, self.twitter_regex)

    def _handle_ios(self, url):
        return self._handle_with_regex(url, self.ios_regex)

    def get_gathered_resources(self, only_best_resources=True):
        dic = {}
        for resource_name, (gathered_resource_set, _) in self.supported_resources.items():
            if gathered_resource_set:
                sorted_resources = list(sorted(gathered_resource_set, key=cmp_to_key(
                    lambda item1, item2:
                    fuzz.ratio(item2.lower(), self.keyword_for_fuzzy_sort) - fuzz.ratio(
                        item1.lower(),
                        self.keyword_for_fuzzy_sort))))
                best_fit = sorted_resources[0] if sorted_resources else None
                dic[resource_name] = best_fit if only_best_resources else sorted_resources
        return dic
