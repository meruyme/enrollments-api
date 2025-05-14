from fastapi import APIRouter
from starlette.responses import JSONResponse, RedirectResponse

from app.core.settings import Settings
from app.routers import v1

settings = Settings()
router = APIRouter(prefix=settings.prefix)
router.include_router(v1.router)


@router.get("/")
def docs_redirect():
    return RedirectResponse(url=settings.prefix + "/docs")
