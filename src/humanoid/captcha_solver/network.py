from __future__ import annotations

import typing
from collections.abc import Mapping
from urllib.error import HTTPError
from urllib.request import Request, urlopen

import requests
from typing_extensions import TypedDict


# pylint: disable=consider-alternative-union-syntax,deprecated-typing-alias
class NetworkRequest(TypedDict):
    url: str
    post_data: typing.Optional[typing.MutableMapping[str, str | float]]


# pylint: enable=consider-alternative-union-syntax,deprecated-typing-alias


class NetworkResponse(TypedDict):
    code: int
    body: bytes
    url: str


def request(
    url: str, data: None | Mapping[str, str | float], timeout: float
) -> NetworkResponse:
    prepared = requests.Request("POST", url, data=data).prepare() if data else None
    req_data = prepared.body if prepared is not None else None
    if isinstance(req_data, str):
        req_data = req_data.encode("ascii")
    req = Request(url, req_data)
    try:
        with urlopen(req, timeout=timeout) as resp:  # nosec B310
            body = resp.read()
            code = resp.getcode()
    except HTTPError as ex:
        code = ex.code
        body = ex.fp.read()
    return {
        "code": code,
        "body": body,
        "url": url,
    }
