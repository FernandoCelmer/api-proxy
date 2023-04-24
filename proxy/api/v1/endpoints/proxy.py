from fastapi import APIRouter, Depends
from fastapi.encoders import jsonable_encoder
from fastapi.responses import Response

from proxy.core.database.mongodb import get_mongodb
from proxy.schemas.proxy import Schema, SchemaBase


router = APIRouter()


@router.post("/proxy", response_model=SchemaBase, status_code=201)
async def create(proxy: Schema, client=Depends(get_mongodb)):
    proxy = jsonable_encoder(proxy)

    try:
        collection = client.proxy[proxy.get("host")]
        await collection.insert_one(proxy)
    except Exception:
        return Response(status_code=422)
    
    return proxy
