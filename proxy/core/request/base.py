"""
Module Base Request
"""

from json import dumps
from requests import request, HTTPError


class BaseRequest:

    def __init__(self, *args, **kwargs) -> None:
        self.method = None
        self.url = None

        self.params = {}
        self.headers = {}
        self.body = {
            "content-type": "application/json"
        }

        for arg in kwargs:
            setattr(self, arg, kwargs.get(arg))

        self.setup()

    def setup_method(self):
        self.method = self.method

    def setup_url(self):
        self.url = self.url

    def setup_params(self):
        self.params = self.params

    def setup_headers(self):
        self.headers = self.headers

    async def setup_body(self):
        self.body = self.body

    def setup(self):
        self.setup_method()
        self.setup_url()

        self.setup_params()
        self.setup_headers()

    async def make_request(
            self,
            method: str = None,
            url: str = None,
            params: dict = {},
            headers: dict = {},
            body: dict = {},
            max_retry: int = 5,
            retry: int = 0):
        kwargs = {
            'method': self.method or method,
            'url': self.url or url,
            'params': self.params or params,
            'headers': self.headers or headers,
            'data': dumps(self.body) or dumps(body)
        }

        def is_server_error(code):
            return 500 <= code <= 599

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
