from typing import List

from fastapi import HTTPException, status

from app.repositories.enrollment import EnrollmentRepository
from app.schemas.enrollment import EnrollmentCreate, EnrollmentRead


class EnrollmentService:
    def __init__(self, enrollment_repository: EnrollmentRepository):
        self.repository = enrollment_repository

    def create(self, enrollment_payload: EnrollmentCreate, username: str) -> EnrollmentRead:
        return self.repository.create(enrollment_payload, username)

    def get(self, enrollment_id: str, username: str) -> EnrollmentRead:
        enrollment = self.repository.get(enrollment_id, username)

        if not enrollment:
            raise HTTPException(
                detail="Enrollment not found.", status_code=status.HTTP_404_NOT_FOUND,
            )

        return enrollment

    def list(self, username: str) -> List[EnrollmentRead]:
        return self.repository.list(username)
