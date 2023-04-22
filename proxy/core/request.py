"""
Module File
"""

from json import dumps
from fastapi.responses import JSONResponse, Response
from requests import request, HTTPError
from urllib.parse import urlsplit, parse_qs

from proxy.core.status import is_server_error
from proxy.core.settings import Settings


class BaseRequest:

    def __init__(self, request) -> None:
        self.request = request

        self.client = {}
        self.proxy = {}
        self.path = {}

        self.method = None
        self.url_proxy = None
        self.url_target = None

        self.params = {}
        self.body = {}
        self.headers = {}

        self.setup()

    def setup_client(self):
        self.client = self.config["USERS"].get(
            self.request.client.host,
            self.client
        )

    def setup_method(self):
        self.method = self.request.method

    def setup_url_proxy(self):
        self.url_proxy = urlsplit(
            url=self.request.headers.get("referer"))

    def setup_url_target(self):
        for client in self.client:
            for path in client.get("paths"):
                if self.url_proxy.path == path.get("path"):
                    self.proxy = self.config["PROXY"].get(client.get("host"))
                    self.path = path
                    break

        if self.proxy:
            self.url_target = "{scheme}://{host}{path}".format(
                scheme=self.proxy.get("scheme"),
                host=self.proxy.get("host"),
                path=path.get("path")
            )

    def setup_params(self):
        dict_params = parse_qs(self.url_proxy.query)
        for param in dict_params:
            dict_params[param] = dict_params[param][0]

        self.params = dict_params

    def setup_headers(self):
        for header in self.request.headers:
            self.headers[header] = self.request.headers.get(header)
        try:
            item_pop = [
                "host",
                "referer",
                "postman-token",
                "accept-encoding",
                "user-agent",
                "accept",
                "connection"
            ]
            for item in item_pop:
                if self.headers.get(item):
                    self.headers.pop(item)
        except Exception:
            pass

    def setup(self):
        self.config = Settings.load()

        self.setup_client()
        self.setup_url_proxy()
        self.setup_url_target()
        self.setup_headers()
        self.setup_params()
        self.setup_method()

    def validate(self):
        if not self.path:
            return Response(status_code=401)

    async def setup_body(self):
        try:
            return await self.request.json()
        except Exception:
            pass

    async def make_request(self, max_retry: int = 5, retry: int = 0):
        if self.validate():
            return self.validate()

        kwargs = {
            'method': self.method,
            'url': self.url_target,
            'params': self.params,
            'headers': self.headers,
            'data': dumps(self.body)
        }

        try:
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
            try:
                return JSONResponse(
                    content=base_response.json(),
                    status_code=base_response.status_code)
            except Exception:
                return Response(
                    status_code=base_response.status_code)

        except Exception:
            return Response(status_code=422)

    async def get(self):
        return await self.make_request()
    
    async def post(self):
        self.body = await self.setup_body()
        return await self.make_request()

    async def put(self):
        self.body = await self.setup_body()
        return await self.make_request()

    async def patch(self):
        self.body = await self.setup_body()
        return await self.make_request()

    async def delete(self):
        return await self.make_request()
