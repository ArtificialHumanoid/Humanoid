from __future__ import annotations

import ssl
from typing import Any

import requests
import urllib3


class HTTPAdapter(requests.adapters.HTTPAdapter):
    """Adapt via `ssl_context`."""

    def __init__(self, ssl_context: ssl.SSLContext | None = None, **kwargs: Any) -> None:
        self.ssl_context = ssl_context or ssl.create_default_context(
            ssl.Purpose.SERVER_AUTH
        )
        self.ssl_context.check_hostname = False
        super().__init__(**kwargs)

    def init_poolmanager(
        self, connections: int, maxsize: int, block: bool = False, **pool_kwargs: Any
    ) -> None:
        self.poolmanager = urllib3.poolmanager.PoolManager(
            num_pools=connections,
            maxsize=maxsize,
            block=block,
            ssl_context=self.ssl_context,
            **pool_kwargs
        )

    @classmethod
    def legacy_session(cls) -> requests.Session:
        context = ssl.create_default_context(ssl.Purpose.SERVER_AUTH)
        context.options |= 0x4  # OP_LEGACY_SERVER_CONNECT
        session = requests.session()
        session.mount("https://", cls(context))
        return session
