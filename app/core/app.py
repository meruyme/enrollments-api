from fastapi import FastAPI, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse, Response

from app.core.settings import Settings
from app.routers import router


async def invalid_data(_: Request, exc: Exception) -> Response:
    return JSONResponse(status_code=422, content={"error": str(exc)})


async def internal_error(_: Request, exc: Exception) -> Response:
    return JSONResponse(status_code=500, content={"error": str(exc)})


def init_app(settings: Settings) -> FastAPI:
    exception_handlers = {
        RequestValidationError: invalid_data,
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
