from typing import Annotated

from pydantic import BeforeValidator, AfterValidator, Field

from app.utils import validate_cpf

PyObjectId = Annotated[str, Field(alias="_id"), BeforeValidator(str)]

Age = Annotated[int, Field(ge=0, lt=150)]

Cpf = Annotated[str, Field(pattern=r"^\d{3}\.\d{3}\.\d{3}\-\d{2}$"), AfterValidator(validate_cpf)]
