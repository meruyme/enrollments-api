from fastapi import APIRouter

from app.routers.v1 import enrollment

router = APIRouter(prefix="/v1")
router.include_router(enrollment.router)
