"""
Module Request Proxy
"""

import logging

from fastapi.responses import JSONResponse, Response
from proxy.core.request import BaseRequest


class RequestProxy(BaseRequest):

    async def proxy_request(self):
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
        return await self.proxy_request()

    async def put(self):
        return await self.proxy_request()

    async def patch(self):
        return await self.proxy_request()

    async def delete(self):
        return await self.proxy_request()
