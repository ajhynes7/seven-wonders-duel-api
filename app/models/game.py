from sqlmodel import Field, SQLModel


class Game(SQLModel, table=True):
    id: int = Field(primary_key=True, default=None)
    date: str
