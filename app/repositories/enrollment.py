from datetime import datetime
from typing import List, Optional

from bson import ObjectId
from pydantic import TypeAdapter
from pymongo.synchronous.database import Database

from app.core.constants import EnrollmentStatus
from app.schemas.enrollment import EnrollmentCreate, EnrollmentRead
from app.schemas.filters import EnrollmentFilter


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
        filter_query = EnrollmentFilter(
            id=enrollment_id,
            username=username,
        )
        filters = self.__build_filter(filter_query)
        enrollment = self.collection.find_one(filters)

        if not enrollment:
            return None

        return EnrollmentRead(**enrollment)

    def list(self, filter_query: EnrollmentFilter = None) -> List[EnrollmentRead]:
        filters = self.__build_filter(filter_query)
        enrollments = self.collection.find(filters)
        return TypeAdapter(List[EnrollmentRead]).validate_python(enrollments)

    @staticmethod
    def __build_filter(filter_query: EnrollmentFilter) -> dict:
        filters = {}
        if filter_query:
            if filter_query.id:
                filters["_id"] = ObjectId(filter_query.id)
            if filter_query.username:
                filters["requested_by"] = filter_query.username
            if filter_query.cpf:
                filters["cpf"] = filter_query.cpf,
            if filter_query.status:
                filters["status"] = {
                    "$in": filter_query.status,
                }
            if filter_query.name:
                filters["name"] = {
                    "$regex": filter_query.name,
                    "$options": "i",
                }
        return filters
