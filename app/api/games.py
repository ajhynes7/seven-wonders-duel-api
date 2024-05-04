from fastapi import APIRouter, Depends
from sqlmodel import Session
from sqlmodel.sql.expression import select

from app.api.util import get_session
from app.models.game import Game

router = APIRouter()


@router.get("/games")
def get_games(session: Session = Depends(get_session)):
    statement = select(Game)
    games = session.exec(statement).all()

    return games


@router.post("/games", status_code=201)
def add_game(game: Game, session: Session = Depends(get_session)):
    session.add(game)
    session.commit()
    session.refresh(game)

    return game
