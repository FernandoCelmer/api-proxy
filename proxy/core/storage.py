"""
Module Storage
"""

from urllib.parse import urlsplit
from proxy.core.database.mongodb import get_mongodb
from proxy.core.error import ErrorProcessProxy


class Storage:

    def __init__(self, request) -> None:
        self.request = request
        self.method = None

        self.url_proxy = None
        self.url_target = None
        self.address_client = None

        self.data_client = []
        self.data_proxy = {}
        self.client_path = {}

    async def build(self):
        try:
            self.data = await get_mongodb()

            self.setup_method()
            self.setup_url_proxy()
            self.setup_address_client()
            await self.setup_data_client()
            await self.setup_data_proxy()

            return {
                "method": self.method,
                "url_proxy": self.url_proxy,
                "url_target": self.url_target,
                "address_client": self.address_client,
                "data_client": self.data_client,
                "data_proxy": self.data_proxy,
                "client_path": self.client_path
            }

        except Exception:
            raise ErrorProcessProxy()
    
    def setup_method(self):
        self.method = self.request.method

    def setup_url_proxy(self):
        temp_referer = self.request.headers.get("referer")
        temp_url = self.request.url

        self.url_proxy = urlsplit(
            url=str(temp_referer or temp_url))

    def setup_address_client(self):
        self.address_client = self.request.client.host

    def set_url_target(self, path: str):
        if self.data_proxy:
            self.url_target = "{scheme}://{host}{path}".format(
                scheme=self.data_proxy.get("scheme"),
                host=self.data_proxy.get("host"),
                path=path
            )

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
                            self.set_url_target(path=url_path)
                            break
                    except Exception:
                        pass

                # Full 'Path' validation.
                if self.url_proxy.path == path.get("path"):
                    self.data_proxy = await self.data.proxy["proxy"].find_one({"host": client.get("host")})
                    self.client_path = path
                    self.set_url_target(path=path.get("path"))
                    break
