from datetime import datetime
from typing import List, Optional

from bson import ObjectId
from pydantic import TypeAdapter
from pymongo.synchronous.database import Database

from app.core.constants import EnrollmentStatus
from app.schemas.enrollment import EnrollmentCreate, EnrollmentRead


class EnrollmentRepository:
    def __init__(self, db: Database):
        self.collection = db.enrollments

    def create(self, enrollment_payload: EnrollmentCreate, username: str) -> EnrollmentRead:
        enrollment_data = enrollment_payload.model_dump()
        enrollment_data.update({
            "requested_by": username,
            "requested_at": datetime.now(),
            "status": EnrollmentStatus.IN_QUEUE,
        })

        enrollment = self.collection.insert_one(enrollment_data)

        return EnrollmentRead(id=str(enrollment.inserted_id), **enrollment_data)

    def get(self, enrollment_id: str, username: str) -> Optional[EnrollmentRead]:
        enrollment = self.collection.find_one({"_id": ObjectId(enrollment_id), "requested_by": username})

        if not enrollment:
            return None

        return EnrollmentRead(**enrollment)

    def list(self, username: str) -> List[EnrollmentRead]:
        enrollments = self.collection.find({"requested_by": username})
        return TypeAdapter(List[EnrollmentRead]).validate_python(enrollments)
