from sqlmodel import Field, SQLModel


class Score(SQLModel, table=True):
    id: int = Field(primary_key=True, default=None)

    game_id: int = Field(foreign_key="game.id")
    player_id: int = Field(foreign_key="player.id")

    civilian: int
    science: int
    commerce: int
    guilds: int
    wonders: int
    tokens: int
    coins: int
    military: int
