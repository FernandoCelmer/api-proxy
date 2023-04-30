from typing import List
from fastapi import APIRouter, Depends, Body, status
from fastapi.encoders import jsonable_encoder
from fastapi.responses import Response

from proxy.core.database.mongodb import get_mongodb
from proxy.schemas.client import SchemaClient, SchemaClientBase


router = APIRouter()


@router.get("/client", response_model=List[SchemaClient], status_code=200)
async def read(user: str, db=Depends(get_mongodb)):
    response = await db.client["client"].find({"user": user}).to_list(1000)
    return response


@router.get("/client/{_id}", response_model=SchemaClient, status_code=200)
async def read_by_id(_id: str, db=Depends(get_mongodb)):
    if (response := await db.client["client"].find_one({"_id": _id})) is not None:
        return response
    return Response(status_code=status.HTTP_404_NOT_FOUND)


@router.post("/client", response_model=SchemaClient, status_code=201)
async def create(client: SchemaClient = Body(...), db=Depends(get_mongodb)):
    client = jsonable_encoder(client)

    if (await db.client["client"].find_one({"user": client.get("user"), "host": client.get("host")})) is not None:
        return Response(status_code=status.HTTP_409_CONFLICT)

    try:
        collection = db.client["client"]
        await collection.insert_one(client)
    except Exception:
        return Response(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY)
    return client


@router.put("/client/{_id}", response_model=SchemaClient)
async def update(_id: str, client: SchemaClientBase = Body(...), db=Depends(get_mongodb)):
    client = jsonable_encoder(client)

    if (await db.client["client"].find_one({"_id": _id})) is not None:
        await db.client["client"].update_one({"_id": _id}, {"$set": client})
        client["_id"] = _id
        return client
    return Response(status_code=status.HTTP_409_CONFLICT)


@router.delete("/client/{_id}")
async def delete(_id: str, db=Depends(get_mongodb)):
    delete_result = await db.client["client"].delete_one({"_id": _id})

    if delete_result.deleted_count == 1:
        return Response(status_code=status.HTTP_204_NO_CONTENT)
    raise Response(status_code=status.HTTP_404_NOT_FOUND)
