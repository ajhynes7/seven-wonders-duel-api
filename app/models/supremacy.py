from enum import Enum

from sqlmodel import Field, SQLModel


class SupremacyType(str, Enum):

    military = "military"
    scientific = "scientific"


class Supremacy(SQLModel, table=True):

    __tablename__: str = "supremacy"

    game_id: int = Field(foreign_key="game.id", primary_key=True)
    player_id: int = Field(foreign_key="player.id")

    type: SupremacyType
