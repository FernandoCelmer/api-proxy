"""
Module Validate
"""

from proxy.core.metrics import metric
from proxy.core.request import RequestPrometheus
from proxy.core.error import (
    ErrorSetupValidate,
    ErrorManyRequests
)


class Validate:


    def __init__(self, *args, **kwargs) -> None:
        self.action = RequestPrometheus()
        self.metric = {}

        for arg in kwargs:
            setattr(self, arg, kwargs.get(arg))

        metric.register_user(
            params=dict(
                client=self.address_client,
                path=self.client_path.get("path"),
                full_path=self.url_proxy.path
            )
        )

    async def setup_metric(self):
        metric = await self.action.get(
                client=self.address_client,
                path=self.client_path.get("path"))

        self.metric = metric.json().get("data")

    async def setup_validate(self):
        if self.metric.get("result"):
            value_request = int(self.metric.get("result")[0]["value"][1])

            # Validation by maximum quantity linked to the user
            if value_request >= self.client_path.get("max_request"):
                raise ErrorManyRequests()

            # Validation by maximum quantity linked to the proxy
            for proxy_path in self.data_proxy["paths"]:
                if self.client_path.get("path") == proxy_path.get("path"):
                    if value_request >= proxy_path.get("max_request"):
                        raise ErrorManyRequests()

    async def setup(self):
        try:
            await self.setup_metric()
            await self.setup_validate()
        except Exception:
            raise ErrorSetupValidate()
