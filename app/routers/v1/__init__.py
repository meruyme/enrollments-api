from fastapi import APIRouter

from app.routers.v1 import counter

router = APIRouter(prefix="/v1")
router.include_router(counter.router)
