"""
Module Request Prometheus
"""

from proxy.core.request.base import BaseRequest
from proxy.core.settings import Settings


class RequestPrometheus(BaseRequest):

    def __init__(self, request=None) -> None:
        self.config = Settings.load_variables()
        super().__init__(request)

    def setup_url(self):
        self.url = "{url_prometheus}/api/v1/query".format(
            url_prometheus=self.config.get("url_prometheus")
        )

    def setup_params(self, client=None, path=None):
        query = f"user_total[job='proxy-api', client='{client}', path='{path}']"
        self.params = {
            "query": query.replace("[", "{").replace("]", "}")
        }

    async def get(self, client: str, path: str):
        self.setup_params(client=client, path=path)
        return await self.make_request(
            method="GET"
        )
