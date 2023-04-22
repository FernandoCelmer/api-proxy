from fastapi import APIRouter, Request

router = APIRouter()


@router.get("/client", include_in_schema=True)
async def client(request: Request):
    """Response IP Address"""
    return {
        "host": request.client.host,
        "port": request.client.port
    }
