"""Search via Google."""
import warnings
from requests import get
import requests.exceptions
import urllib3.exceptions
from bs4 import BeautifulSoup
from time import sleep
from .user_agents import get_useragent
import re


def _req(term, results, lang, start, proxies, timeout, verify=True):
    resp = get(
        url="https://www.google.com/search",
        headers={
            "User-Agent": get_useragent()
        },
        params={
            "q": term,
            "num": results + 2,  # Prevents multiple requests
            "hl": lang,
            "start": start,
        },
        proxies=proxies,
        timeout=timeout,
        verify=verify
    )
    resp.raise_for_status()
    return resp


class SearchResult:
    def __init__(self, url, title, description=None):
        self.url = url
        self.title = title
        self.description = description

    def __repr__(self):
        return f"SearchResult(url={self.url}, title={self.title}, description={self.description})"


search_url_regex = re.compile("/search\?.*q=")


def search(term, num_results=10, lang="en", proxy=None, advanced=False, sleep_interval=0, timeout=5, verify=True):
    """Search via Google."""
    import urllib.parse

    escaped_term = term

    # Proxy
    proxies = None
    if proxy:
        if proxy.startswith("https"):
            proxies = {"https": proxy}
        else:
            proxies = {"http": proxy}

    # Fetch
    start = 0
    while start < num_results:
        # Send request
        try:
            resp = _req(escaped_term, num_results - start, lang, start, proxies, timeout, verify)
        except requests.exceptions.ConnectionError:
            warnings.warn("Failed to connect.")
            return

        # Parse
        soup = BeautifulSoup(resp.text, "html.parser")
        result_block = soup.find_all("div")
        if not result_block:
            warnings.warn("There are less than the requested number of results.")
            break
        for result in result_block:
            if "class" in result.attrs:
                # Find link, title, description box
                link = result.find("a", href=True)
                title = result.find("h3")
                description_box = result.find("div", {"style": "-webkit-line-clamp:2"})
                if link and title and description_box:
                    search_url = search_url_regex.search(link.attrs["href"])
                    if not search_url:
                        start += 1
                        if advanced:
                            yield SearchResult(link["href"], title.text, getattr(description_box, text, None))
                        else:
                            yield link["href"]
        sleep(sleep_interval)


if __name__ == "__main__":
    pass
