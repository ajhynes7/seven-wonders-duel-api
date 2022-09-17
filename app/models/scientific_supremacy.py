from sqlmodel import Field, SQLModel


class ScientificSupremacy(SQLModel, table=True):

    __tablename__: str = "scientific_supremacy"

    id: int = Field(primary_key=True, default=None)

    game_id: int
    player_id: int
