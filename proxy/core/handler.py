"""
Module Handler
"""

import logging

from urllib.parse import parse_qs, urlsplit
from proxy.core.database.mongodb import get_mongodb
from proxy.core.error import ErrorSetupStorage


class Handler:

    def __init__(self, request) -> None:
        self.request = request
        self.method = None

        self.url_proxy = None
        self.url = None
        self.address_client = None

        self.params = {}
        self.headers = {}
        self.body = {}

        self.data_client = []
        self.data_proxy = {}
        self.client_path = {}

    async def setup(self):
        try:
            self.data = await get_mongodb()

            self.setup_method()
            self.setup_url_proxy()
            self.setup_address_client()
            self.setup_params()
            self.setup_headers()

            await self.setup_body()
            await self.setup_data_client()
            await self.setup_data_proxy()

            return {
                "method": self.method,
                "url": self.url,
                "url_proxy": self.url_proxy,
                "address_client": self.address_client,
                "data_client": self.data_client,
                "data_proxy": self.data_proxy,
                "client_path": self.client_path,
                "params": self.params,
                "headers": self.headers,
                "body": self.body
            }

        except Exception:
            raise ErrorSetupStorage()

    def setup_method(self):
        self.method = self.request.method

    def setup_url_proxy(self):
        temp_referer = self.request.headers.get("referer")
        temp_url = self.request.url

        self.url_proxy = urlsplit(
            url=str(temp_referer or temp_url))

    def setup_address_client(self):
        self.address_client = self.request.client.host

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

    def set_url(self, path: str):
        if self.data_proxy:
            self.url = "{scheme}://{host}{path}".format(
                scheme=self.data_proxy.get("scheme"),
                host=self.data_proxy.get("host"),
                path=path
            )

    async def setup_body(self):
        try:
            self.body = await self.request.json()
        except Exception as error:
            logging.error(error)

    async def setup_data_client(self):
        self.data_client = await self.data.client["client"].find(
            {"user": self.address_client}).to_list(1000)

    async def setup_data_proxy(self):
        for client in self.data_client:
            for path in client.get("paths"):

                # Validation of 'Path' with 'ID'.
                url_id = urlsplit(self.url_proxy.path).path.split('/')[-1].split('.')[0]
                if url_id:
                    try:
                        url_path = path.get("path").format(ID=url_id)
                        if self.url_proxy.path == url_path:
                            self.data_proxy = await self.data.proxy["proxy"].find_one({"host": client.get("host")})
                            self.client_path = path
                            self.set_url(path=url_path)
                            break
                    except Exception:
                        pass

                # Full 'Path' validation.
                if self.url_proxy.path == path.get("path"):
                    self.data_proxy = await self.data.proxy["proxy"].find_one({"host": client.get("host")})
                    self.client_path = path
                    self.set_url(path=path.get("path"))
                    break
