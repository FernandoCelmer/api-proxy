from fastapi import APIRouter, Depends, Body, status
from fastapi.encoders import jsonable_encoder
from fastapi.responses import Response

from proxy.core.database.mongodb import get_mongodb
from proxy.schemas.proxy import SchemaProxy, SchemaProxyBase


router = APIRouter()


@router.get("/proxy", response_model=SchemaProxy, status_code=200)
async def read(host: str, client=Depends(get_mongodb)):
    if (response := await client.proxy["proxy"].find_one({"host": host})) is not None:
        return response
    return Response(status_code=status.HTTP_404_NOT_FOUND)


@router.get("/proxy/{_id}", response_model=SchemaProxy, status_code=200)
async def read_by_id(_id: str, client=Depends(get_mongodb)):
    if (response := await client.proxy["proxy"].find_one({"_id": _id})) is not None:
        return response
    return Response(status_code=status.HTTP_404_NOT_FOUND)


@router.post("/proxy", response_model=SchemaProxy, status_code=201)
async def create(proxy: SchemaProxy = Body(...), client=Depends(get_mongodb)):
    proxy = jsonable_encoder(proxy)

    if (await client.proxy["proxy"].find_one({"host": proxy.get("host")})) is not None:
        return Response(status_code=status.HTTP_409_CONFLICT)

    try:
        collection = client.proxy["proxy"]
        await collection.insert_one(proxy)
    except Exception:
        return Response(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY)
    return proxy


@router.put("/proxy/{_id}", response_model=SchemaProxy)
async def update(_id: str, proxy: SchemaProxyBase = Body(...), client=Depends(get_mongodb)):
    proxy = jsonable_encoder(proxy)

    if (await client.proxy["proxy"].find_one({"_id": _id})) is not None:
        await client.proxy["proxy"].update_one({"_id": _id}, {"$set": proxy})
        proxy["_id"] = _id
        return proxy
    return Response(status_code=status.HTTP_409_CONFLICT)


@router.delete("/proxy/{_id}")
async def delete(_id: str, client=Depends(get_mongodb)):
    delete_result = await client.proxy["proxy"].delete_one({"_id": _id})

    if delete_result.deleted_count == 1:
        return Response(status_code=status.HTTP_204_NO_CONTENT)
    raise Response(status_code=status.HTTP_404_NOT_FOUND)
