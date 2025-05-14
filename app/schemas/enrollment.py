from datetime import datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict

from app.core.constants import EnrollmentStatus
from app.fields import PyObjectId, Cpf, Age


class EnrollmentBase(BaseModel):
    name: str
    age: Age
    cpf: Cpf

    model_config = ConfigDict(
        str_strip_whitespace=True
    )


class EnrollmentCreate(EnrollmentBase):
    ...


class EnrollmentRead(EnrollmentBase):
    id: PyObjectId
    requested_at: datetime
    requested_by: str
    finished_at: Optional[datetime] = None
    status: EnrollmentStatus
