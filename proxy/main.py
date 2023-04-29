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
async def custom_http_exception_handler(request, exception):
    client_host = request.client.host
    client_header = request.headers.get("client")

    metric.register(
        method=request.method.lower(),
        params=dict(
            client=client_host or client_header,
            path=request.url.path
        )
    )
    return RedirectResponse(
        url=f"/redirect?{request.url.query}")
