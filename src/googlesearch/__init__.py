import warnings
from bs4 import BeautifulSoup
from requests import get
from time import sleep
from .user_agents import get_useragent
import re


def _req(term, results, lang, start, proxies):
    resp = get(
        url="https://www.google.com/search",
        headers={
            "User-Agent": get_useragent()
        },
        params=dict(
            q=term,
            num=results + 2,  # Prevents multiple requests
            hl=lang,
            start=start,
        ),
        proxies=proxies,
    )
    if __debug__:
        print(resp.request.url)
    resp.raise_for_status()
    return resp


class SearchResult:
    def __init__(self, url, title):
        self.url = url
        self.title = title

    def __repr__(self):
        return f"SearchResult(url={self.url}, title={self.title})"


def search(term, num_results=10, lang="en", proxy=None, advanced=False, sleep_interval=0):
    escaped_term = term.replace(" ", "+")

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
        resp = _req(escaped_term, num_results - start, lang, start, proxies)

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
                    search_url = "/search?q=" in link.attrs["href"]
                    if not search_url:
                        start += 1
                        if advanced:
                            yield SearchResult(link["href"], title.text)
                        else:
                            yield link["href"]
        sleep(sleep_interval)


if __name__ == "__main__":
    pass
