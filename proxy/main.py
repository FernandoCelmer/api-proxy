from fastapi import FastAPI
from fastapi.responses import RedirectResponse
from starlette.exceptions import HTTPException

from proxy import __version__
from proxy.api.v1.routers import router


app = FastAPI(
    title="API Proxy",
    description="Proxy Project API",
    version=__version__
)

app.include_router(router)


@app.exception_handler(HTTPException)
async def custom_http_exception_handler(request, exception):
    return RedirectResponse(
        url=f"/redirect?{request.url.query}")
