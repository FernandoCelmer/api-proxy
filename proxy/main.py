from fastapi import FastAPI
from fastapi.responses import RedirectResponse
from starlette.exceptions import HTTPException

from proxy import __version__
from proxy.core.metrics import Metric
from proxy.api.v1.routers import router


app = FastAPI(
    title="API Proxy",
    description="Proxy Project API",
    version=__version__
)

app.include_router(router)
metric = Metric()


@app.exception_handler(HTTPException)
async def custom_http_exception_handler(request, exc):
    method = request.method.lower()
    metric.register(
        method=method,
        params=dict(
            client=request.client.host,
            path=request.url.path
        )
    )

    return RedirectResponse(
        url=f"/{method}?{request.url.query}",
        headers=request.headers
    )
