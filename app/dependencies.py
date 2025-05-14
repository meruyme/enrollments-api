from fastapi import Depends
from pymongo.synchronous.database import Database

from app.core.db import DatabaseProvider
from app.repositories.enrollment import EnrollmentRepository
from app.services.enrollment import EnrollmentService


def get_database() -> Database:
    return DatabaseProvider.get_database()


def get_enrollment_repository(db: Database = Depends(get_database)) -> EnrollmentRepository:
    return EnrollmentRepository(db)


def get_enrollment_service(
    enrollment_repository: EnrollmentRepository = Depends(get_enrollment_repository)
) -> EnrollmentService:
    return EnrollmentService(enrollment_repository)
