"""
Module Base Request
"""

from json import dumps
from requests import request, HTTPError
from proxy.core.status import is_server_error


class BaseRequest:

    def __init__(self, request=None) -> None:
        self.request = request
        self.method = None
        self.url_target = None

        self.params = {}
        self.headers = {}
        self.body = {}

        self.setup()

    def setup_method(self):
        self.method = self.method

    def setup_url_target(self):
        self.url_target = self.url_target

    def setup_params(self):
        self.params = self.params

    def setup_headers(self):
        self.headers = self.headers

    def setup(self):
        self.setup_method()
        self.setup_url_target()
        self.setup_params()
        self.setup_headers()

    async def make_request(
            self,
            method: str = None,
            url_target: str = None,
            params: dict = {},
            headers: dict = {},
            body: dict = {},
            max_retry: int = 5,
            retry: int = 0):
        kwargs = {
            'method': self.method or method,
            'url': self.url_target or url_target,
            'params': self.params or params,
            'headers': self.headers or headers,
            'data': dumps(self.body) or dumps(body)
        }

        with request(**kwargs) as response:
            base_response = response

            if is_server_error(base_response.status_code):
                try:
                    response.raise_for_status()
                except HTTPError:
                    if retry < max_retry:
                        retry += 1
                        base_response = await self.make_request(
                            retry=retry
                        )
            return base_response
