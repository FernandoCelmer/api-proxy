from fastapi import APIRouter, Request, Response, status
from proxy.core.request.proxy import RequestProxy
from proxy.core.error import ErrorProcessProxy

router = APIRouter()


@router.get("/redirect", include_in_schema=False)
async def proxy(request: Request):
    """GET Proxy"""
    try:
        return await RequestProxy(request).get()
    except ErrorProcessProxy:
        return Response(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY)


@router.post("/redirect", include_in_schema=False)
async def post_proxy(request: Request):
    """POST Proxy"""
    try:
        return await RequestProxy(request).post()
    except ErrorProcessProxy:
        return Response(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY)


@router.put("/redirect", include_in_schema=False)
async def put_proxy(request: Request):
    """PUT Proxy"""
    try:
        return await RequestProxy(request).put()
    except ErrorProcessProxy:
        return Response(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY)


@router.patch("/redirect", include_in_schema=False)
async def patch_proxy(request: Request):
    """PATCH Proxy"""
    try:
        return await RequestProxy(request).patch()
    except ErrorProcessProxy:
        return Response(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY)


@router.delete("/redirect", include_in_schema=False)
async def delete_proxy(request: Request):
    """DELETE Proxy"""
    try:
        return await RequestProxy(request).delete()
    except ErrorProcessProxy:
        return Response(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY)
