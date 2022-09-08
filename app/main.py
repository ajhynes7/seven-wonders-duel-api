from fastapi import Depends, FastAPI
from sqlmodel import Session, create_engine, select

from app.models.game import Game
from app.models.player import Player
from app.models.score import Score

app = FastAPI()
engine = create_engine("postgresql://localhost:5432/seven_wonders_duel")


def get_session():

    with Session(engine) as session:
        yield session


@app.get("/players")
def get_players(session: Session = Depends(get_session)):

    statement = select(Player)
    players = session.exec(statement).all()

    return players


@app.get("/games")
def get_games(session: Session = Depends(get_session)):

    statement = select(Game)
    games = session.exec(statement).all()

    return games


@app.get("/scores")
def get_scores(
    game_id: int | None = None,
    session: Session = Depends(get_session),
):

    statement = select(Score)

    if game_id:
        statement = statement.where(Score.game_id == game_id)

    scores = session.exec(statement).all()

    return scores


    scores = session.exec(statement).all()

    return scores
