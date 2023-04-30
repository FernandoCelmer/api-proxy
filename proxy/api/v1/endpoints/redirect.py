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


@router.get("/redirect", include_in_schema=False)
async def proxy(request: Request):
    """GET Proxy"""
    try:
        storage = await Handler(request=request).setup()
        await Validate(**storage).setup()

        return await RequestProxy(**storage).get()

    except ErrorSetupStorage:
        return Response(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY)
    
    except ErrorSetupValidate:
        return Response(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY)
    
    except ErrorManyRequests:
        return Response(
            status_code=status.HTTP_429_TOO_MANY_REQUESTS)


@router.post("/redirect", include_in_schema=False)
async def post_proxy(request: Request):
    """POST Proxy"""
    try:
        storage = await Handler(request=request).setup()
        await Validate(**storage).setup()

        return await RequestProxy(**storage).post()

    except ErrorSetupStorage:
        return Response(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY)
    
    except ErrorSetupValidate:
        return Response(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY)
    
    except ErrorManyRequests:
        return Response(
            status_code=status.HTTP_429_TOO_MANY_REQUESTS)


@router.put("/redirect", include_in_schema=False)
async def put_proxy(request: Request):
    """PUT Proxy"""
    try:
        storage = await Handler(request=request).setup()
        await Validate(**storage).setup()

        return await RequestProxy(**storage).put()

    except ErrorSetupStorage:
        return Response(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY)
    
    except ErrorSetupValidate:
        return Response(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY)
    
    except ErrorManyRequests:
        return Response(
            status_code=status.HTTP_429_TOO_MANY_REQUESTS)


@router.patch("/redirect", include_in_schema=False)
async def patch_proxy(request: Request):
    """PATCH Proxy"""
    try:
        storage = await Handler(request=request).setup()
        await Validate(**storage).setup()

        return await RequestProxy(**storage).patch()

    except ErrorSetupStorage:
        return Response(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY)
    
    except ErrorSetupValidate:
        return Response(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY)
    
    except ErrorManyRequests:
        return Response(
            status_code=status.HTTP_429_TOO_MANY_REQUESTS)


@router.delete("/redirect", include_in_schema=False)
async def delete_proxy(request: Request):
    """DELETE Proxy"""
    try:
        storage = await Handler(request=request).setup()
        await Validate(**storage).setup()

        return await RequestProxy(**storage).delete()

    except ErrorSetupStorage:
        return Response(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY)
    
    except ErrorSetupValidate:
        return Response(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY)
    
    except ErrorManyRequests:
        return Response(
            status_code=status.HTTP_429_TOO_MANY_REQUESTS)