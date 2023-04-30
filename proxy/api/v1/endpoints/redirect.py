from fastapi import APIRouter, Request, Response, status
from proxy.core.request.proxy import RequestProxy
from proxy.core.error import (
    ErrorSetupStorage,
    ErrorSetupValidate,
    ErrorManyRequests
)

from proxy.core.handler import Handler
from proxy.core.validate import Validate

router = APIRouter()


async def proyx_handler(request):
    try:
        storage = await Handler(request=request).setup()
        await Validate(**storage).setup()

        return await RequestProxy(**storage).proxy_request()

    except ErrorSetupStorage:
        return Response(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY)

    except ErrorSetupValidate:
        return Response(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY)

    except ErrorManyRequests:
        return Response(
            status_code=status.HTTP_429_TOO_MANY_REQUESTS)


@router.get("/redirect", include_in_schema=False)
async def proxy(request: Request):
    """GET Proxy"""
    return await proyx_handler(request=request)


@router.post("/redirect", include_in_schema=False)
async def post_proxy(request: Request):
    """POST Proxy"""
    return await proyx_handler(request=request)


@router.put("/redirect", include_in_schema=False)
async def put_proxy(request: Request):
    """PUT Proxy"""
    return await proyx_handler(request=request)


@router.patch("/redirect", include_in_schema=False)
async def patch_proxy(request: Request):
    """PATCH Proxy"""
    return await proyx_handler(request=request)


@router.delete("/redirect", include_in_schema=False)
async def delete_proxy(request: Request):
    """DELETE Proxy"""
    return await proyx_handler(request=request)
