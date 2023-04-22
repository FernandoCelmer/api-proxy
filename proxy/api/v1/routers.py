from fastapi import APIRouter
from proxy.api.v1.endpoints import proxy, metrics, client

router = APIRouter()


router.include_router(proxy.router, tags=["Proxy"])
router.include_router(metrics.router, tags=["Metrics"])
router.include_router(client.router, tags=["Client"])
