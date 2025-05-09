from typing import List

from fastapi import APIRouter, Depends, status

from app.dependencies import get_enrollment_service
from app.schemas.enrollment import EnrollmentRead, EnrollmentCreate
from app.services.enrollment import EnrollmentService
from app.auth import get_current_username

router = APIRouter(
    prefix="/enrollments",
    tags=["Enrollment API V1"],
)


@router.post(
    "/",
    response_model=EnrollmentRead,
    status_code=status.HTTP_201_CREATED,
)
def create_enrollment(
    payload: EnrollmentCreate,
    service: EnrollmentService = Depends(get_enrollment_service),
    current_username: str = Depends(get_current_username),
):
    return service.create(payload, current_username)


@router.get(
    "/{enrollment_id}/",
    response_model=EnrollmentRead,
    status_code=status.HTTP_200_OK,
)
def get_enrollment(
    enrollment_id: str,
    service: EnrollmentService = Depends(get_enrollment_service),
    current_username: str = Depends(get_current_username),
):
    return service.get(enrollment_id, current_username)


@router.get(
    "/",
    response_model=List[EnrollmentRead],
    status_code=status.HTTP_200_OK,
)
def list_enrollment(
    service: EnrollmentService = Depends(get_enrollment_service),
    current_username: str = Depends(get_current_username),
):
    return service.list(current_username)
