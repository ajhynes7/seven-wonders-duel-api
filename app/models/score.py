from sqlmodel import Field, SQLModel


class Score(SQLModel, table=True):
    game_id: int = Field(foreign_key="game.id", primary_key=True)
    player_id: int = Field(foreign_key="player.id", primary_key=True)

    civilian: int
    science: int
    commerce: int
    guilds: int
    wonders: int
    tokens: int
    coins: int
    military: int
