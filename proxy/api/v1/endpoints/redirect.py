from fastapi import APIRouter, Request
from proxy.core.request.proxy import RequestProxy

router = APIRouter()


@router.get("/redirect", include_in_schema=False)
async def proxy(request: Request):
    """GET Proxy"""
    return await RequestProxy(request).get()


@router.post("/redirect", include_in_schema=False)
async def post_proxy(request: Request):
    """POST Proxy"""
    return await RequestProxy(request).post()


@router.put("/redirect", include_in_schema=False)
async def put_proxy(request: Request):
    """PUT Proxy"""
    return await RequestProxy(request).put()


@router.patch("/redirect", include_in_schema=False)
async def patch_proxy(request: Request):
    """PATCH Proxy"""
    return await RequestProxy(request).patch()


@router.delete("/redirect", include_in_schema=False)
async def delete_proxy(request: Request):
    """DELETE Proxy"""
    return await RequestProxy(request).delete()
