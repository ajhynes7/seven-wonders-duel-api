import re

from pydantic import validator
from sqlmodel import Field, SQLModel


class Game(SQLModel, table=True):
    id: int = Field(primary_key=True, default=None)
    date: str

    @validator("date")
    def date_must_have_specific_format(cls, input: str) -> str:

        pattern = r"\d{4}-\d{2}-\d{2}"
        match = re.fullmatch(pattern, input)

        if not match:
            raise ValueError("The date must have the format YYYY-MM-DD.")

        return input
