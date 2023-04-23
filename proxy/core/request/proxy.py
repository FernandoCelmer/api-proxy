"""
Module Request Proxy
"""

import logging

from urllib.parse import parse_qs, urlsplit
from fastapi.responses import JSONResponse, Response
from proxy.core.request.base import BaseRequest
from proxy.core.request.prometheus import RequestPrometheus
from proxy.core.settings import Settings


class RequestProxy(BaseRequest):

    def __init__(self, request) -> None:
        self.data = Settings.load_data()

        self.url_proxy = None
        self.client = {}
        self.proxy = {}
        self.client_path = {}
        super().__init__(request)

    def setup_client(self):
        self.client = self.data["users"].get(
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
                    self.proxy = self.data["proxy"].get(client.get("host"))
                    self.client_path = path
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

        except Exception as error:
            logging.error(error)

    def setup(self):
        self.setup_client()
        self.setup_url_proxy()
        self.setup_url_target()
        self.setup_headers()
        self.setup_params()
        self.setup_method()

    async def validate(self):
        if not self.client_path:
            return Response(status_code=401)

        try:
            action = RequestPrometheus()
            metric = await action.prometheus_request(
                client=self.request.client.host,
                path=self.client_path.get("path")
            )

            metric = metric.json().get("data")
            if metric.get("result"):
                value_request = int(metric.get("result")[0]["value"][1])

                # Validation by maximum quantity linked to the user - file users.json
                if value_request >= self.client_path.get("max_request"):
                    return Response(status_code=401)

                # Validation by maximum quantity linked to the proxy - file proxy.json
                for proxy_path in self.proxy["paths"]:
                    if proxy_path == proxy_path.get("path"):
                        if value_request >= proxy_path.get("max_request"):
                            return Response(status_code=401)

        except Exception as error:
            logging.error(error)
            return Response(status_code=401)

    async def setup_body(self):
        try:
            return await self.request.json()
        except Exception as error:
            logging.error(error)

    async def proxy_request(self):
        if await self.validate():
            return await self.validate()

        try:
            base_response = await self.make_request()
            try:
                return JSONResponse(
                    content=base_response.json(),
                    status_code=base_response.status_code)

            except Exception as error:
                logging.error(error)
                return Response(
                    status_code=base_response.status_code)

        except Exception as error:
            logging.error(error)
            return Response(status_code=422)

    async def get(self):
        return await self.proxy_request()

    async def post(self):
        self.body = await self.setup_body()
        return await self.proxy_request()

    async def put(self):
        self.body = await self.setup_body()
        return await self.proxy_request()

    async def patch(self):
        self.body = await self.setup_body()
        return await self.proxy_request()

    async def delete(self):
        return await self.proxy_request()
