from typing import List

from fastapi import HTTPException, status

from app.core.constants import EnrollmentStatus
from app.core.rabbitmq import RabbitMQProvider
from app.repositories.enrollment import EnrollmentRepository
from app.schemas.enrollment import EnrollmentCreate, EnrollmentRead
from app.schemas.filters import EnrollmentFilter


class EnrollmentService:
    def __init__(self, enrollment_repository: EnrollmentRepository):
        self.repository = enrollment_repository

    def create(self, enrollment_payload: EnrollmentCreate, username: str) -> EnrollmentRead:
        if self.__exists_enrollment_for_cpf(enrollment_payload):
            raise HTTPException(
                detail="This CPF already has an enrollment in queue or accepted.",
                status_code=status.HTTP_400_BAD_REQUEST,
            )

        enrollment = self.repository.create(enrollment_payload, username)

        RabbitMQProvider().publish_message(enrollment.id)

        return enrollment

    def get(self, enrollment_id: str, username: str) -> EnrollmentRead:
        enrollment = self.repository.get(enrollment_id, username)

        if not enrollment:
            raise HTTPException(
                detail="Enrollment not found.", status_code=status.HTTP_404_NOT_FOUND,
            )

        return enrollment

    def list(self, username: str, filter_query: EnrollmentFilter) -> List[EnrollmentRead]:
        filter_query.username = username
        return self.repository.list(filter_query)

    def __exists_enrollment_for_cpf(self, enrollment_payload: EnrollmentCreate) -> bool:
        filter_query = EnrollmentFilter(
            cpf=enrollment_payload.cpf,
            status=[EnrollmentStatus.IN_QUEUE, EnrollmentStatus.ACCEPTED],
        )
        return bool(self.repository.list(filter_query))
