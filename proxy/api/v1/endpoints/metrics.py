from fastapi import APIRouter
from fastapi.responses import PlainTextResponse
from prometheus_client import generate_latest

router = APIRouter()


@router.get("/metrics", include_in_schema=True)
async def get_metrics():
    return PlainTextResponse(generate_latest())
