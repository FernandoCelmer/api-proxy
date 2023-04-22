from urllib import parse
from fastapi import APIRouter, Request
from proxy.core.request import BaseRequest

router = APIRouter()


@router.get("/proxy", include_in_schema=False)
async def proxy(request: Request):
    """GET API Proxy"""
    return await BaseRequest(request).get()


@router.post("/proxy", include_in_schema=False)
async def post_proxy(request: Request):
    """POST Proxy"""
    return await BaseRequest(request).post()


@router.put("/proxy", include_in_schema=False)
async def put_proxy(request: Request):
    """PUT Proxy"""
    return await BaseRequest(request).put()


@router.patch("/proxy", include_in_schema=False)
async def patch_proxy(request: Request):
    """PATCH Proxy"""
    return await BaseRequest(request).patch()


@router.delete("/proxy", include_in_schema=False)
async def delete_proxy(request: Request):
    """DELETE Proxy"""
    return await BaseRequest(request).make_request()
