from typing import Annotated

from pydantic import BaseModel, ConfigDict, Field, BeforeValidator

PyObjectId = Annotated[str, BeforeValidator(str)]


class Counter(BaseModel):
    counter: int
    total_calls: int

    model_config = ConfigDict(
        str_strip_whitespace=True
    )


class CounterRead(Counter):
    id: PyObjectId = Field(alias="_id")
