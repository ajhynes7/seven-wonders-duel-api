from sqlmodel import Field, SQLModel


class MilitarySupremacy(SQLModel, table=True):

    __tablename__: str = "military_supremacy"

    id: int = Field(primary_key=True, default=None)

    game_id: int
    player_id: int
