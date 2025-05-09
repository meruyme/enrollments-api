from fastapi import FastAPI, Request
from fastapi.exceptions import HTTPException
from fastapi.responses import JSONResponse, Response

from app.core.settings import Settings
from app.routers import router


async def internal_error(_: Request, exc: Exception) -> Response:
    return JSONResponse(status_code=500, content={"error": str(exc)})


async def http_exception_handler(_: Request, exc: HTTPException) -> Response:
    return JSONResponse(status_code=exc.status_code, content={"error": exc.detail})


def init_app(settings: Settings) -> FastAPI:
    exception_handlers = {
        HTTPException: http_exception_handler,
        Exception: internal_error,
    }

    app = FastAPI(
        title=settings.api_name,
        version=settings.api_version,
        openapi_url=settings.prefix + "/openapi.json",
        docs_url=settings.prefix + "/docs",
        redoc_url=None,
        exception_handlers=exception_handlers,
    )

    app.include_router(router)
    return app
