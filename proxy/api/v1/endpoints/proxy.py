from urllib import parse
from fastapi import APIRouter, Request

router = APIRouter()


@router.get("/get", include_in_schema=False)
async def get_proxy(request: Request):
    """GET API Proxy"""
    return ({"method": "POST"})


@router.post("/post", include_in_schema=False)
async def post_proxy(request: Request):
    """POST Proxy"""
    return ({"method": "POST"})


@router.put("/put", include_in_schema=False)
async def put_proxy(request: Request):
    """PUT Proxy"""
    return ({"method": "PUT"})


@router.patch("/patch", include_in_schema=False)
async def patch_proxy(request: Request):
    """PATCH Proxy"""
    return ({"method": "PATCH"})


@router.delete("/delete", include_in_schema=False)
async def delete_proxy(request: Request):
    """DELETE Proxy"""
    return ({"method": "DELETE"})
