import ssl

import requests
import urllib3


class HTTPAdapter(requests.adapters.HTTPAdapter):
    """
    Adapt via `ssl_context`.
    """

    def __init__(self, ssl_context=None, **kwargs):
        self.ssl_context = ssl_context
        self.ssl_context.check_hostname = False
        super().__init__(**kwargs)

    def init_poolmanager(self, connections, maxsize, block=False):
        self.poolmanager = urllib3.poolmanager.PoolManager(
            num_pools=connections, maxsize=maxsize, block=block, ssl_context=self.ssl_context)

    @classmethod
    def legacy_session(cls):
        context = ssl.create_default_context(ssl.Purpose.SERVER_AUTH)
        context.options |= 0x4  # OP_LEGACY_SERVER_CONNECT
        session = requests.session()
        session.mount('https://', cls(context))
        return session
