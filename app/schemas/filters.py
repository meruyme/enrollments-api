from typing import Optional, List
from pydantic import BaseModel

from app.core.constants import EnrollmentStatus
from app.fields import Cpf


class EnrollmentFilter(BaseModel):
    name: Optional[str] = None
    cpf: Optional[Cpf] = None
    status: Optional[List[EnrollmentStatus]] = None
