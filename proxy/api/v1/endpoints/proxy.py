from fastapi import APIRouter, Request
from proxy.core.request.proxy import RequestProxy

router = APIRouter()


@router.get("/proxy", include_in_schema=False)
async def proxy(request: Request):
    """GET Proxy"""
    return await RequestProxy(request).get()


@router.post("/proxy", include_in_schema=False)
async def post_proxy(request: Request):
    """POST Proxy"""
    return await RequestProxy(request).post()


@router.put("/proxy", include_in_schema=False)
async def put_proxy(request: Request):
    """PUT Proxy"""
    return await RequestProxy(request).put()


@router.patch("/proxy", include_in_schema=False)
async def patch_proxy(request: Request):
    """PATCH Proxy"""
    return await RequestProxy(request).patch()


@router.delete("/proxy", include_in_schema=False)
async def delete_proxy(request: Request):
    """DELETE Proxy"""
    return await RequestProxy(request).delete()
