"""
Module Request Prometheus
"""

from proxy.core.request.base import BaseRequest
from proxy.core.settings import Settings


class RequestPrometheus(BaseRequest):

    def __init__(self, request=None) -> None:
        self.config = Settings.load_variables()
        super().__init__(request)

    def setup_method(self):
        self.method = 'GET'

    def setup_url_target(self):
        url_prometheus = self.config.get("url_prometheus")
        self.url_target = f"{url_prometheus}/api/v1/query"

    def setup_params(self, client=None, path=None):
        query = f"get_total[job='proxy-api', client='{client}', path='{path}']"
        self.params = {
            "query": query.replace("[", "{").replace("]", "}")
        }

    def setup_headers(self):
        self.headers = {
            "content-type": "application/json"
        }

    async def prometheus_request(self, client: str, path: str):
        self.setup_params(client=client, path=path)
        return await self.make_request()
