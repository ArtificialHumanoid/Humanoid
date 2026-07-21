from __future__ import annotations

from unittest import TestCase
from unittest.mock import Mock, patch

import requests

from humanoid.actions import internet_search
from humanoid.actions.internet_search import google


class InternetSearchTestCase(TestCase):
    def test_request_verifies_certificates_by_default(self) -> None:
        response = Mock(spec=requests.Response)

        with (
            patch.object(google, "get_useragent", return_value="test-agent"),
            patch.object(requests, "get", return_value=response) as request_get,
            patch.object(internet_search.HTTPAdapter, "legacy_session") as legacy,
        ):
            result = google._req("query", 1, "en", 0, None, 5)

        self.assertIs(result, response)
        legacy.assert_not_called()
        request_get.assert_called_once_with(
            url="https://www.google.com/search",
            headers={"User-Agent": "test-agent"},
            params={"q": "query", "num": 3, "hl": "en", "start": 0},
            proxies=None,
            timeout=5,
            verify=True,
        )
        response.raise_for_status.assert_called_once_with()

    def test_request_uses_legacy_session_when_verification_is_disabled(self) -> None:
        response = Mock(spec=requests.Response)
        session = Mock(spec=requests.Session)
        session.get.return_value = response

        with (
            patch.object(google, "get_useragent", return_value="test-agent"),
            patch.object(requests, "get") as request_get,
            patch.object(
                internet_search.HTTPAdapter,
                "legacy_session",
                return_value=session,
            ) as legacy,
        ):
            result = google._req("query", 1, "en", 0, None, 5, verify=False)

        self.assertIs(result, response)
        request_get.assert_not_called()
        legacy.assert_called_once_with()
        session.get.assert_called_once_with(
            url="https://www.google.com/search",
            headers={"User-Agent": "test-agent"},
            params={"q": "query", "num": 3, "hl": "en", "start": 0},
            proxies=None,
            timeout=5,
            verify=False,
        )
        response.raise_for_status.assert_called_once_with()

    def test_search_forwards_disabled_verification(self) -> None:
        response = Mock(spec=requests.Response)
        response.text = (
            '<div class="result"><a href="https://example.com">'
            "<h3>Example</h3></a>"
            '<div style="-webkit-line-clamp:2">Description</div></div>'
        )

        with patch.object(google, "_req", return_value=response) as request:
            results = list(google.search("query", num_results=1, verify=False))

        self.assertEqual(results, ["https://example.com"])
        request.assert_called_once_with("query", 1, "en", 0, None, 5, False)

    def test_legacy_ssl_context_supports_unverified_requests(self) -> None:
        context = internet_search._legacy_ssl_context()

        self.assertFalse(context.check_hostname)
        self.assertTrue(
            context.options & internet_search._OP_LEGACY_SERVER_CONNECT
        )
