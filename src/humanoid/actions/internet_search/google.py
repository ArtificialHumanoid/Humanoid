"""Search via Google."""
from __future__ import annotations

import re
import warnings
from collections.abc import Iterator
from time import sleep

import requests
import requests.exceptions
from bs4 import BeautifulSoup

from humanoid.credential_management import get_useragent
from humanoid.actions.internet_search import HTTPAdapter


def _req(
    term: str,
    results: int,
    lang: str,
    start: int,
    proxies: dict[str, str] | None,
    timeout: float,
    verify: bool = True,
) -> requests.Response:
    headers = {
        "User-Agent": get_useragent(),
    }
    params: dict[str, str | int] = {
        "q": term,
        "num": results + 2,  # Prevents multiple requests
        "hl": lang,
        "start": start,
    }

    if verify:
        resp = requests.get(
            url="https://www.google.com/search",
            headers=headers,
            params=params,
            proxies=proxies,
            timeout=timeout,
            verify=verify,
        )
    else:
        resp = HTTPAdapter.legacy_session().get(
            url="https://www.google.com/search",
            headers=headers,
            params=params,
            proxies=proxies,
            timeout=timeout,
            verify=verify,
        )
    resp.raise_for_status()
    return resp


class SearchResult:
    def __init__(
        self, url: str, title: str, description: str | None = None
    ) -> None:
        self.url = url
        self.title = title
        self.description = description

    def __repr__(self) -> str:
        return (
            f"SearchResult(url={self.url}, title={self.title}, "
            f"description={self.description})"
        )


search_url_regex = re.compile(r"/search\?.*q=")


def search(
    term: str,
    num_results: int = 10,
    lang: str = "en",
    proxy: str | None = None,
    advanced: bool = False,
    sleep_interval: float = 0,
    timeout: float = 5,
    verify: bool = True,
) -> Iterator[str | SearchResult]:
    """Search via Google."""
    escaped_term = term

    # Proxy
    proxies: dict[str, str] | None = None
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
            resp = _req(
                escaped_term,
                num_results - start,
                lang,
                start,
                proxies,
                timeout,
                verify,
            )
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
                    href = link.get("href")
                    if not isinstance(href, str):
                        continue
                    search_url = search_url_regex.search(href)
                    if not search_url:
                        start += 1
                        if advanced:
                            yield SearchResult(
                                href,
                                title.get_text(),
                                description_box.get_text() or None,
                            )
                        else:
                            yield href
        sleep(sleep_interval)


if __name__ == "__main__":
    pass
